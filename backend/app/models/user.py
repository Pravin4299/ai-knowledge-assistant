import uuid

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import String

from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.base import SoftDeleteMixin
from sqlalchemy.orm import relationship

class User(
    Base,
    TimestampMixin,
    SoftDeleteMixin
):
    __tablename__ = "users"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String,
        nullable=False
    )

    role = Column(
        String,
        default="user",
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    chat_sessions = relationship(
        "ChatSession",
        backref="user"
    )