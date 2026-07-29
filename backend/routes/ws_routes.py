import asyncio
from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

# Keep WebSocket payloads aligned with the HTTP chat endpoint's 2,000-character limit.
MAX_WEBSOCKET_MESSAGE_SIZE = 2_000


class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self._lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        async with self._lock:
            self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        async with self._lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        async with self._lock:
            connections = list(self.active_connections)
        for connection in connections:
            try:
                await connection.send_text(message)
            except (ConnectionError, RuntimeError, WebSocketDisconnect):
                await self.disconnect(connection)


manager = ConnectionManager()


@router.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    """Handles real-time WebSocket chat."""
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            if len(data) > MAX_WEBSOCKET_MESSAGE_SIZE:
                await websocket.close(code=1009, reason="Message too large")
                break
            await manager.broadcast(data)
    except WebSocketDisconnect:
        pass
    finally:
        await manager.disconnect(websocket)
