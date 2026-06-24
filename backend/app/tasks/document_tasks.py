

from app.core.database import SessionLocal

from app.repositories.document_repository import (
    DocumentRepository
)

from app.services.document_processing_service import (
    DocumentProcessingService
)

def process_document_background(
    document_id: str
):

    db = SessionLocal()

    try:

        document = (
            DocumentRepository.get_by_id(
                db,
                document_id
            )
        )

        if document:

            DocumentProcessingService.process_document(
                db=db,
                document=document
            )

    finally:

        db.close()
