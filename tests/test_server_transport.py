import asyncio

import pytest

from server import ChatServer


class MemoryWriter:
    def __init__(self, slow: bool = False) -> None:
        self.buffer = bytearray()
        self.slow = slow
        self.closed = False

    def write(self, data: bytes) -> None:
        self.buffer.extend(data)

    async def drain(self) -> None:
        if self.slow:
            await asyncio.Event().wait()

    def close(self) -> None:
        self.closed = True

    async def wait_closed(self) -> None:
        return None

    def get_extra_info(self, name: str):
        return ("127.0.0.1", 9999) if name == "peername" else None


@pytest.mark.asyncio
async def test_newline_framing_handles_split_and_coalesced_frames() -> None:
    server = ChatServer()
    reader = asyncio.StreamReader()
    pending = asyncio.create_task(server._read_frame(reader, None))
    reader.feed_data(b'{"user":"a"')
    await asyncio.sleep(0)
    reader.feed_data(b',"text":"one"}\n{"user":"b","text":"two"}\n')
    assert await pending == b'{"user":"a","text":"one"}'
    assert await server._read_frame(reader, None) == b'{"user":"b","text":"two"}'


@pytest.mark.asyncio
async def test_oversized_frame_is_rejected() -> None:
    server = ChatServer()
    reader = asyncio.StreamReader(limit=4)
    reader.feed_data(b"123456\n")
    assert await server._read_frame(reader, None) is None


@pytest.mark.asyncio
async def test_malformed_json_is_not_broadcast(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("REQUIRE_AUTH", "false")
    server = ChatServer()
    reader = asyncio.StreamReader()
    writer = MemoryWriter()
    reader.feed_data(b"not-json\n")
    reader.feed_eof()
    await server.handle_client(reader, writer)
    assert not writer.buffer
    assert writer.closed


@pytest.mark.asyncio
async def test_slow_consumer_is_dropped(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("server.DRAIN_TIMEOUT_S", 0.001)
    server = ChatServer()
    writer = MemoryWriter(slow=True)
    server.active.add(writer)
    await server._safe_write(writer, b"payload")
    assert writer.closed
    assert writer not in server.active


@pytest.mark.asyncio
async def test_auth_handshake_accepts_valid_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("REQUIRE_AUTH", "true")
    monkeypatch.setenv("AUTH_TOKEN", "secret")
    monkeypatch.setenv("AUTH_IDENTITY", "server-user")
    server = ChatServer()
    reader = asyncio.StreamReader()
    writer = MemoryWriter()
    reader.feed_data(b'{"type":"auth","token":"secret","user":"spoofed"}\n')
    assert await server._authenticate(reader, writer, None)
    assert server.identities[writer] == "server-user"


@pytest.mark.asyncio
async def test_auth_handshake_rejects_invalid_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("REQUIRE_AUTH", "true")
    monkeypatch.setenv("AUTH_TOKEN", "secret")
    server = ChatServer()
    reader = asyncio.StreamReader()
    writer = MemoryWriter()
    reader.feed_data(b'{"type":"auth","token":"incorrect"}\n')
    assert not await server._authenticate(reader, writer, None)
