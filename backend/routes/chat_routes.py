from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from backend.services.chat_service import ChatService

router = APIRouter()

chat_service = ChatService()

# -------------------------------------------
#  Pydantic Models (request/response schemas)
# -------------------------------------------

class MessageRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    username: str = Field(min_length=1, max_length=32, pattern=r"^[\w .'-]+$")
    content: str = Field(min_length=1, max_length=2_000)


class MessageResponse(BaseModel):
    id: str
    username: str
    content: str
    timestamp: str


# -------------------------------------------
#  Routes
# -------------------------------------------

@router.post("/send", response_model=MessageResponse)
async def send_message(message: MessageRequest):
    """
    Sends a chat message to the realtime storage layer.
    """
    try:
        new_message = chat_service.send_message(
            username=message.username,
            content=message.content
        )
        return new_message
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Message store unavailable") from exc


@router.get("/history")
async def get_message_history(limit: int = 50):
    """
    Returns the latest N chat messages.
    """
    try:
        if not 1 <= limit <= 200:
            raise HTTPException(status_code=422, detail="limit must be between 1 and 200")
        messages = chat_service.get_messages(limit=limit)
        return messages
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Message store unavailable") from exc
