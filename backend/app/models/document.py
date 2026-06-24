import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.base import SoftDeleteMixin


class Document(
    Base,
    TimestampMixin,
    SoftDeleteMixin
):
    __tablename__ = "documents"

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

    filename = Column(
        String,
        nullable=False
    )

    file_type = Column(
        String,
        nullable=False
    )

    file_size = Column(
        Integer,
        nullable=False
    )

    file_path = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="uploaded",
        nullable=False
    )

    processing_status = Column(
        String,
        nullable=False,
        default="pending"
    )