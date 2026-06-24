from datetime import datetime

from pydantic import BaseModel


class CreateMessageRequest(BaseModel):
    session_id: str
    content: str


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }