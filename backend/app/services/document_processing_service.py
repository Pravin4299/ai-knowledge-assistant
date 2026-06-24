from app.models.document_chunk import DocumentChunk
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository
)
from app.services.chunking_service import (
    ChunkingService
)
from app.services.document_parser_service import (
    DocumentParserService
)
from app.services.embedding_service import (
    EmbeddingService
)
from app.repositories.document_repository import(
    DocumentRepository
)
class DocumentProcessingService:

    @staticmethod
    def process_document(
        db,
        document
    ):

        try:
            print("STEP 1: processing started")
            DocumentRepository.update_status(
                db,
                document,
                "processing"
            )
            print("STEP 2: extracting text")
            text = (
                DocumentParserService.extract_text(
                    file_path=document.file_path,
                    file_type=document.file_type
                )
            )
            print("STEP 3: chunking")
            chunks = ChunkingService.split_text(
                text=text
            )

            chunk_objects = []


            for index, chunk in enumerate(chunks):

                embedding = (
                    EmbeddingService.create_embedding(
                        chunk
                    )
                )

                chunk_objects.append(
                    DocumentChunk(
                        document_id=document.id,
                        chunk_index=index,
                        chunk_text=chunk,
                        embedding=embedding
                    )
                )
            DocumentChunkRepository.bulk_create(
                db=db,
                chunks=chunk_objects
            )

            DocumentChunkRepository.update_search_vectors(
                db=db,
                document_id=document.id
            )

            DocumentRepository.update_status(
                db,
                document,
                "completed"
            )
            print("STEP 7: completed")
            document.status = "completed"

            db.commit()
        
        except Exception:

            DocumentRepository.update_status(
                db,
                document,
                "failed"
            )

            raise
