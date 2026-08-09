from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router

# --------------------------------------------------
# App Initialization
# --------------------------------------------------
app = FastAPI(
    title="TrojanChat 2.0 AI",
    description="AI-powered USC fan chat platform with RAG and real-time insights",
    version="2.0.0",
)

# --------------------------------------------------
# Middleware (CORS for frontend connection)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the AI chat router under /api/chat
app.include_router(chat_router, prefix="/api/chat", tags=["AI Chat"])


# --------------------------------------------------
# Health Endpoints
# --------------------------------------------------
@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "TrojanChat 2.0 AI is running",
        "status": "healthy",
        "version": "2.0.0",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "service": "trojanchat-backend",
    }
