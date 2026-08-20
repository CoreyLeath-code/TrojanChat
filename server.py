"""Single-process asyncio broadcast server with newline-delimited JSON framing."""
from __future__ import annotations

import asyncio
import json
import logging
import os
import signal
import ssl
import sys
from datetime import datetime, timezone
from typing import Any

from backendsecurity import BackendSecurityManager

MAX_MESSAGE_BYTES = int(os.getenv("MAX_MESSAGE_BYTES", str(64 * 1024)))
DRAIN_TIMEOUT_S = float(os.getenv("DRAIN_TIMEOUT_S", "5"))
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8888"))

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] Server: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)


class ChatServer:
    """Single-process async broadcast server for newline-delimited JSON messages."""

    def __init__(self, host: str = HOST, port: int = PORT) -> None:
        self.host = host
        self.port = port
        self.active: set[asyncio.StreamWriter] = set()
        self._server: asyncio.AbstractServer | None = None

    @staticmethod
    def tls_context_from_environment() -> ssl.SSLContext | None:
        cert_file = os.getenv("TLS_CERT_FILE")
        key_file = os.getenv("TLS_KEY_FILE")
        if not cert_file and not key_file:
            log.warning("TLS disabled; set TLS_CERT_FILE and TLS_KEY_FILE to enable it.")
            return None
        if not cert_file or not key_file:
            raise ValueError("TLS_CERT_FILE and TLS_KEY_FILE must be set together.")

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        return context

    async def _audit(self, event_type: str, details: str, peer: Any) -> None:
        BackendSecurityManager.audit_security_event(
            event_type=event_type, details=details, IP_peer=peer
        )

    async def _read_frame(
        self, reader: asyncio.StreamReader, peer: Any
    ) -> bytes | None:
        try:
            frame = await reader.readuntil(b"\n")
        except asyncio.IncompleteReadError:
            return None
        except asyncio.LimitOverrunError as error:
            await self._audit("OVERSIZED_FRAME_REJECTED", str(error), peer)
            return None

        if len(frame) > MAX_MESSAGE_BYTES:
            await self._audit("OVERSIZED_FRAME_REJECTED", "frame exceeds limit", peer)
            return None
        return frame[:-1]

    async def _safe_write(self, writer: asyncio.StreamWriter, payload: bytes) -> None:
        try:
            writer.write(payload + b"\n")
            await asyncio.wait_for(writer.drain(), timeout=DRAIN_TIMEOUT_S)
        except (ConnectionError, asyncio.TimeoutError) as error:
            log.info("Dropping slow or disconnected client: %s", error)
            await self.disconnect_client(writer)
        except Exception:
            log.exception("Unexpected client write failure")
            await self.disconnect_client(writer)

    async def broadcast(
        self, message: dict[str, Any], exclude_writer: asyncio.StreamWriter | None = None
    ) -> None:
        payload = json.dumps(message, separators=(",", ":")).encode("utf-8")
        recipients = [
            self._safe_write(writer, payload)
            for writer in list(self.active)
            if writer is not exclude_writer
        ]
        if recipients:
            await asyncio.gather(*recipients, return_exceptions=True)

    async def handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        peer = writer.get_extra_info("peername")
        self.active.add(writer)
        log.info("Client connected: %s", peer)
        try:
            while frame := await self._read_frame(reader, peer):
                try:
                    secure = BackendSecurityManager.validate_and_sanitize_payload(frame)
                except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
                    await self._audit("MALFORMED_INPUT_REJECTED", str(error), peer)
                    continue

                await self.broadcast(
                    {
                        "user": secure["user"],
                        "text": secure["text"],
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    },
                    exclude_writer=writer,
                )
        except (ConnectionError, asyncio.TimeoutError) as error:
            log.info("Client connection ended: %s", error)
        except asyncio.CancelledError:
            raise
        except Exception:
            log.exception("Unexpected client processing failure")
        finally:
            await self.disconnect_client(writer)

    async def disconnect_client(self, writer: asyncio.StreamWriter) -> None:
        self.active.discard(writer)
        writer.close()
        try:
            await writer.wait_closed()
        except (ConnectionError, asyncio.TimeoutError):
            pass

    async def close(self) -> None:
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
        await asyncio.gather(
            *(self.disconnect_client(writer) for writer in list(self.active)),
            return_exceptions=True,
        )

    async def start(self) -> None:
        self._server = await asyncio.start_server(
            self.handle_client,
            self.host,
            self.port,
            ssl=self.tls_context_from_environment(),
            limit=MAX_MESSAGE_BYTES,
        )
        log.info(
            "Single-process async broadcast server listening on tcp://%s:%s",
            self.host,
            self.port,
        )
        async with self._server:
            await self._server.serve_forever()


async def main() -> None:
    server = ChatServer()
    loop = asyncio.get_running_loop()
    stop = asyncio.Event()
    for signal_name in (signal.SIGINT, getattr(signal, "SIGTERM", signal.SIGINT)):
        try:
            loop.add_signal_handler(signal_name, stop.set)
        except NotImplementedError:
            pass
    task = asyncio.create_task(server.start())
    await stop.wait()
    task.cancel()
    await asyncio.gather(task, return_exceptions=True)
    await server.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
