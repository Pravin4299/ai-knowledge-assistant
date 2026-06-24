from app.repositories.document_chunk_repository import (
    DocumentChunkRepository
)
from app.services.embedding_service import (
    EmbeddingService
)


class RetrievalService:

    @staticmethod
    def retrieve(
        db,
        user_id:str,
        question: str,
        top_k: int = 5
    ):

        query_embedding = (
            EmbeddingService.create_embedding(
                question
            )
        )

        # return (
        #     DocumentChunkRepository
        #     .similarity_search(
        #         db=db,
        #         user_id=user_id,
        #         query_embedding=query_embedding,
        #         limit=top_k
        #     )
        # )
    
        results = (
            DocumentChunkRepository.similarity_search(
                db=db,
                user_id=user_id,
                query_embedding=query_embedding,
                limit=top_k
            )
        )

        results = [
            result
            for result in results
            if result["distance"] < 0.75
        ]

        return results