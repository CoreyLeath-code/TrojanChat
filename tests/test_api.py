"""Tests for the FastAPI app: chat endpoint, health check, and structured JSON."""
import pytest
from httpx import AsyncClient, ASGITransport
from app.core.main import app


@pytest.mark.asyncio
async def test_root_returns_running_message():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "TrojanChat API is running" in response.text


@pytest.mark.asyncio
async def test_root_returns_structured_json():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    data = response.json()
    assert "message" in data
    assert "version" in data


@pytest.mark.asyncio
async def test_health_check_returns_ok():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "trojanchat-backend"


@pytest.mark.asyncio
async def test_chat_send_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/chat/send",
            json={"username": "TrojanFan", "content": "Fight On!"}
        )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "TrojanFan"
    assert data["content"] == "Fight On!"
    assert "id" in data
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_chat_history_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/chat/history?limit=50")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
