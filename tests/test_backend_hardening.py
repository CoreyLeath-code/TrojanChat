"""Unit and integration coverage for bounded storage and API trust boundaries."""

import asyncio
from unittest.mock import AsyncMock

import pytest
from backend.api import app
from backend.routes.ws_routes import ConnectionManager
from backend.services.chat_service import ChatService
from httpx import ASGITransport, AsyncClient


def test_store_evicts_oldest_message_and_returns_copy() -> None:
    service = ChatService(max_messages=2)
    service.send_message("a", "one")
    service.send_message("b", "two")
    service.send_message("c", "three")
    history = service.get_messages(50)
    assert [message["content"] for message in history] == ["two", "three"]
    history.clear()
    assert len(service.get_messages(50)) == 2


def test_store_rejects_invalid_capacity_and_nonpositive_limit() -> None:
    with pytest.raises(ValueError, match="positive"):
        ChatService(max_messages=-1)
    assert ChatService(1).get_messages(0) == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"username": "", "content": "hello"},
        {"username": "<script>", "content": "hello"},
        {"username": "user", "content": ""},
        {"username": "user", "content": "x" * 2_001},
        {"username": "user", "content": "hello", "admin": True},
    ],
)
async def test_api_rejects_invalid_messages(payload: dict) -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/chat/send", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_api_bounds_history_queries() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        assert (await client.get("/chat/history?limit=0")).status_code == 422
        assert (await client.get("/chat/history?limit=201")).status_code == 422


@pytest.mark.asyncio
async def test_connection_manager_removes_failed_clients() -> None:
    manager = ConnectionManager()
    healthy = AsyncMock()
    failed = AsyncMock()
    failed.send_text.side_effect = ConnectionError("closed")
    manager.active_connections.extend([healthy, failed])
    await manager.broadcast("hello")
    healthy.send_text.assert_awaited_once_with("hello")
    assert failed not in manager.active_connections


@pytest.mark.asyncio
async def test_connection_manager_connect_and_disconnect() -> None:
    manager = ConnectionManager()
    websocket = AsyncMock()
    await manager.connect(websocket)
    websocket.accept.assert_awaited_once()
    assert websocket in manager.active_connections
    await manager.disconnect(websocket)
    assert websocket not in manager.active_connections
    await asyncio.wait_for(manager.disconnect(websocket), timeout=1)
