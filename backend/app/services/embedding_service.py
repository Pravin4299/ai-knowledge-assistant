from sentence_transformers import (
    SentenceTransformer
)


class EmbeddingService:

    _model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    @classmethod
    def create_embedding(
        cls,
        text: str
    ):
        embedding = cls._model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()