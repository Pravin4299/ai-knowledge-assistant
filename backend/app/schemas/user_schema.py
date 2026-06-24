from datetime import datetime

from pydantic import BaseModel
from pydantic import EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }