import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from app.core.database import Base
from app.models.base import TimestampMixin


class ChatMessage(
    Base,
    TimestampMixin
):
    __tablename__ = "chat_messages"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    session_id = Column(
        String,
        ForeignKey("chat_sessions.id"),
        nullable=False,
        index=True
    )

    role = Column(
        String,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    token_count = Column(
        Integer,
        default=0,
        nullable=False
    )