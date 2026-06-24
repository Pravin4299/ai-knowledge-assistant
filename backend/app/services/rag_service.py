from app.services.retrieval_service import (
    RetrievalService
)
from app.services.llm_service import (LLMService)
class RAGService:

    @staticmethod
    def answer(
        db,
        question: str
    ):
        chunks = RetrievalService.retrieve(
            db=db,
            question=question,
            top_k=3
        )

        context = "\n\n".join(
            chunk["chunk_text"]
            for chunk in chunks
        )

        prompt = f"""
Use ONLY the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

        return LLMService.generate_text(
            prompt
        )