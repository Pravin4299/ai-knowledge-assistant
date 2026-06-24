from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.document_chunk import DocumentChunk


class DocumentChunkRepository:

    @staticmethod
    def bulk_create(
        db: Session,
        chunks: list[DocumentChunk]
    ):
        db.bulk_save_objects(chunks)
        db.commit()

    @staticmethod
    def get_document_chunks(
        db: Session,
        document_id: str
    ):
        return (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == document_id
            )
            .order_by(
                DocumentChunk.chunk_index.asc()
            )
            .all()
        )
    
    @staticmethod
    def similarity_search(
        db,
        user_id: str,
        query_embedding,
        limit=5
    ):
        sql = text("""
            SELECT
                dc.id,
                dc.document_id,
                d.filename,
                dc.chunk_index,
                dc.chunk_text,
                dc.embedding <=> CAST(:embedding AS vector) AS distance
            FROM document_chunks dc
            JOIN documents d
                ON dc.document_id = d.id
            WHERE d.user_id = :user_id
            AND d.processing_status = 'completed'
            AND dc.embedding IS NOT NULL
            ORDER BY dc.embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)

        result = db.execute(
            sql,
            {
                "user_id": user_id,
                "embedding": str(query_embedding),
                "limit": limit
            }
        )

        rows = result.fetchall()

        return [
            {
                "id": row[0],
                "document_id": row[1],
                "filename": row[2],
                "chunk_index": row[3],
                "chunk_text": row[4],
                "distance": row[5]
            }
            for row in rows
        ]
    
    @staticmethod
    def keyword_search(
        db,
        user_id: str,
        query: str,
        limit: int = 5
    ):
        sql = text("""
        SELECT
            dc.id,
            dc.document_id,
            d.filename,
            dc.chunk_index,
            dc.chunk_text,
            ts_rank(
                dc.search_vector,
                plainto_tsquery(
                    'english',
                    :query
                )
            ) AS score
        FROM document_chunks dc
        JOIN documents d
            ON d.id = dc.document_id
        WHERE d.user_id = :user_id
        AND dc.search_vector @@
            plainto_tsquery(
                'english',
                :query
            )
        ORDER BY score DESC
        LIMIT :limit
        """)

        result = db.execute(
            sql,
            {
                "user_id": user_id,
                "query": query,
                "limit": limit
            }
        )
        rows = result.fetchall()

        return [
            {
                "id": row[0],
                "document_id": row[1],
                "filename": row[2],
                "chunk_index": row[3],
                "chunk_text": row[4],
                "keyword_score": row[5]
            }
            for row in rows
        ]
    
    @staticmethod
    def delete_by_document_id(
        db,
        document_id: str
    ):
        (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == document_id
            )
            .delete()
        )

        db.commit()

    @staticmethod
    def update_search_vectors(
        db,
        document_id: str
    ):

        sql = text("""
            UPDATE document_chunks
            SET search_vector =
                to_tsvector(
                    'english',
                    chunk_text
                )
            WHERE document_id = :document_id
        """)

        db.execute(
            sql,
            {
                "document_id": document_id
            }
        )

        db.commit()