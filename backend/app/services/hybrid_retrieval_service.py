from app.repositories.document_chunk_repository import (
    DocumentChunkRepository
)

from app.services.embedding_service import (
    EmbeddingService
)

class HybridRetrievalService:

    @staticmethod
    def retrieve(
        db,
        user_id: str,
        question: str,
        top_k: int = 5
    ):
        query_embedding = (
            EmbeddingService.create_embedding(
                question
            )
        )

        vector_results = (
            DocumentChunkRepository
            .similarity_search(
                db=db,
                user_id=user_id,
                query_embedding=query_embedding,
                limit=10
            )
        )
        keyword_results = (
            DocumentChunkRepository
            .keyword_search(
                db=db,
                user_id=user_id,
                query=question,
                limit=10
            )
        )
        merged = {}

        for chunk in vector_results:

            merged[
                chunk["id"]
            ] = {
                **chunk,
                "score": (
                    1 - chunk["distance"]
                )
            }
        
        for chunk in keyword_results:

            if chunk["id"] in merged:

                merged[
                    chunk["id"]
                ]["score"] += (
                    chunk["keyword_score"]
                )

            else:

                merged[
                    chunk["id"]
                ] = {
                    **chunk,
                    "score": chunk["keyword_score"]
                }
        
        results = sorted(
            merged.values(),
            key=lambda x: x["score"],
            reverse=True
        )
        return results[:top_k]