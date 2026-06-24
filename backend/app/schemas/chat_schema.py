from datetime import datetime

from pydantic import BaseModel


class ChatSessionCreate(BaseModel):
    title: str | None = None


class ChatSessionResponse(BaseModel):
    id: str
    title: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class RenameSessionRequest(BaseModel):
    title: str

class MessageResponse(BaseModel):
    success: bool
    message: str