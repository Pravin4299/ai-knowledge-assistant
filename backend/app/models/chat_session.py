import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime

from app.core.database import Base
from app.models.base import SoftDeleteMixin
from app.models.base import TimestampMixin
from sqlalchemy import Text
from sqlalchemy.orm import relationship

class ChatSession(
    Base,
    TimestampMixin,
    SoftDeleteMixin
):
    __tablename__ = "chat_sessions"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    user_id = Column(
        String,
        ForeignKey("users.id"),
        nullable=False
    )

    title = Column(
        String,
        nullable=False,
        default="New Chat"
    )

    last_message_at = Column(
        DateTime,
        nullable=True
    )

    message_count = Column(
        Integer,
        default=0,
        nullable=False
    )
    messages = relationship(
        "ChatMessage",
        backref="session",
        cascade="all, delete-orphan"
    )

    conversation_summary = Column(
        Text,
        nullable=True
    )