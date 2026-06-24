from pydantic import BaseModel


class SourceResponse(
    BaseModel
):
    chunk_index: int
    distance: float


class CitationResponse(
    BaseModel
):
    document_id: str
    filename: str
    chunk_index: int
    distance: float


class RAGResponse(
    BaseModel
):
    answer: str
    sources: list[CitationResponse]