from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    question: str
    is_rag: bool = False

class CitationResponse(
    BaseModel
):
    document_id: str
    filename: str
    chunk_index: int
    distance: float

class ChatResponse(BaseModel):
    answer: str
    sources: list[CitationResponse]