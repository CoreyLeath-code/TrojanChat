from fastapi import FastAPI

from backend.config import settings
from backend.routes.chat_routes import router as chat_router
from backend.routes.ws_routes import router as websocket_router


def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI application.
    Following a factory pattern allows easier testing and expansion.
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.API_VERSION,
        debug=settings.DEBUG
    )

    # Include application routes
    app.include_router(chat_router, prefix="/chat", tags=["Chat"])
    app.include_router(websocket_router, tags=["WebSocket"])

    @app.get("/", tags=["Health"])
    async def root():
        return {
            "message": "TrojanChat API is running",
            "version": settings.API_VERSION
        }

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {
            "status": "ok",
            "service": "trojanchat-backend"
        }

    return app


app = create_app()
