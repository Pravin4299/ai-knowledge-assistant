from pydantic import BaseModel


class DocumentChunkResponse(
    BaseModel
):
    chunk_index: int
    chunk_text: str

    model_config = {
        "from_attributes": True
    }