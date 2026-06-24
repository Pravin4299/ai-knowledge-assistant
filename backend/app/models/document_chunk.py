import uuid

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import String
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import TSVECTOR

from app.core.database import Base
from app.models.base import TimestampMixin


class DocumentChunk(
    Base,
    TimestampMixin
):
    __tablename__ = "document_chunks"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    document_id = Column(
        String,
        ForeignKey("documents.id"),
        nullable=False,
        index=True
    )

    chunk_index = Column(
        Integer,
        nullable=False
    )

    chunk_text = Column(
        Text,
        nullable=False
    )
    embedding = Column(
        Vector(384),
        nullable=True
    )
    search_vector = Column(
        TSVECTOR,
        nullable=True
    )