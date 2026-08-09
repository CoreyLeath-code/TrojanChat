"""
Tests for the AI-powered chat endpoint (/api/chat/).

All external AI dependencies (Groq, Cohere, Qdrant) are mocked via
FastAPI's dependency override system so these tests run in CI without
real API keys or network access.
"""

import pytest
from unittest.mock import MagicMock, patch
from httpx import AsyncClient, ASGITransport


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def _make_mock_engine(response: str = "USC has a strong recruiting class.", success: bool = True):
    """Return a MagicMock whose .run() matches TrojanChatAI's return shape."""
    mock = MagicMock()
    mock.run.return_value = {"success": success, "response": response}
    return mock


@pytest.fixture()
def app_with_mock_ai():
    """
    Yield the backend/app FastAPI app with TrojanChatAI replaced by a mock.

    Uses FastAPI dependency overrides so no real Groq/Cohere/Qdrant calls
    are ever made — even if those packages are installed.
    """
    # Patch TrojanChatAI so importing backend.app.main doesn't try to
    # connect to Groq or Qdrant at module load time.
    with patch("ai.graph.TrojanChatAI.__init__", return_value=None), \
         patch("ai.llm.groq_client.GroqClient.__init__", return_value=None), \
         patch("ai.retrieval.qdrant_search.QdrantSearch.__init__", return_value=None), \
         patch("ai.embeddings.cohere_embedder.CohereEmbedder.__init__", return_value=None):

        from backend.app.main import app
        from backend.app.api.chat import get_ai_engine

        mock_engine = _make_mock_engine()
        app.dependency_overrides[get_ai_engine] = lambda: mock_engine

        yield app, mock_engine

        # Tear down override after test
        app.dependency_overrides.pop(get_ai_engine, None)


# ---------------------------------------------------------------------------
# Route registration
# ---------------------------------------------------------------------------


def test_ai_app_registers_chat_router_once(app_with_mock_ai):
    """The public chat route must have one registration and one handler."""
    app, _ = app_with_mock_ai
    chat_routes = [
        route
        for route in app.routes
        if route.path == "/api/chat/" and "POST" in route.methods
    ]

    assert len(chat_routes) == 1


# ---------------------------------------------------------------------------
# /  — root endpoint
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_ai_app_root_returns_200(app_with_mock_ai):
    app, _ = app_with_mock_ai
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


@pytest.mark.asyncio
async def test_ai_app_root_contains_message(app_with_mock_ai):
    app, _ = app_with_mock_ai
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    data = response.json()
    assert "message" in data, "Root response must include a 'message' key"


# ---------------------------------------------------------------------------
# /health — health-check endpoint
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_ai_app_health_returns_ok(app_with_mock_ai):
    app, _ = app_with_mock_ai
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200, "Health check must return HTTP 200"
    data = response.json()
    assert data.get("status") == "ok", f"Expected status='ok', got {data.get('status')!r}"


@pytest.mark.asyncio
async def test_ai_app_health_has_service_name(app_with_mock_ai):
    app, _ = app_with_mock_ai
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    data = response.json()
    assert "service" in data, "Health response must include a 'service' field"


# ---------------------------------------------------------------------------
# /api/chat/ — AI chat endpoint (happy path)
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_chat_endpoint_returns_200(app_with_mock_ai):
    app, _ = app_with_mock_ai
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/chat/", json={"message": "Who leads USC's receiving corps?"})
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"


@pytest.mark.asyncio
async def test_chat_endpoint_returns_success_true(app_with_mock_ai):
    app, _ = app_with_mock_ai
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/chat/", json={"message": "Fight On!"})
    data = response.json()
    assert data["success"] is True, f"Expected success=True, got {data}"


@pytest.mark.asyncio
async def test_chat_endpoint_returns_response_text(app_with_mock_ai):
    app, _ = app_with_mock_ai
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/chat/", json={"message": "Summarize USC recruiting."})
    data = response.json()
    assert isinstance(data.get("response"), str), "Response must be a non-null string"
    assert len(data["response"]) > 0, "Response text must not be empty"


@pytest.mark.asyncio
async def test_chat_endpoint_calls_ai_engine_once(app_with_mock_ai):
    """Verify the dependency-injected engine is actually invoked."""
    app, mock_engine = app_with_mock_ai
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post("/api/chat/", json={"message": "Preview next game."})
    mock_engine.run.assert_called_once()


@pytest.mark.asyncio
async def test_chat_endpoint_passes_user_message_to_engine(app_with_mock_ai):
    """The exact user message must be forwarded to the AI engine."""
    app, mock_engine = app_with_mock_ai
    user_query = "Who are the top DB recruits this cycle?"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post("/api/chat/", json={"message": user_query})
    mock_engine.run.assert_called_once_with(user_query)


# ---------------------------------------------------------------------------
# /api/chat/ — validation / error handling
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_chat_endpoint_rejects_empty_message(app_with_mock_ai):
    """An empty message string must return HTTP 422 (validation error)."""
    app, _ = app_with_mock_ai
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/chat/", json={"message": "   "})
    assert response.status_code == 422, (
        f"Expected 422 for empty message, got {response.status_code}"
    )


@pytest.mark.asyncio
async def test_chat_endpoint_requires_message_field(app_with_mock_ai):
    """Missing 'message' field must return HTTP 422."""
    app, _ = app_with_mock_ai
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/chat/", json={})
    assert response.status_code == 422, (
        f"Expected 422 for missing message field, got {response.status_code}"
    )


@pytest.mark.asyncio
async def test_chat_endpoint_when_engine_returns_failure(app_with_mock_ai):
    """When the AI engine signals failure, success must be False in the response."""
    app, mock_engine = app_with_mock_ai
    mock_engine.run.return_value = {"success": False, "response": None}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/chat/", json={"message": "Trigger failure."})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False, f"Expected success=False, got {data}"
    assert data["response"] is None
