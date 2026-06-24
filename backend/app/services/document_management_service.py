import os

from app.repositories.document_repository import (
    DocumentRepository
)

from app.repositories.document_chunk_repository import (
    DocumentChunkRepository
)


class DocumentManagementService:

    @staticmethod
    def delete_document(
        db,
        document,
    ):

        if (
            document.file_path
            and
            os.path.exists(document.file_path)
        ):
            os.remove(document.file_path)

        DocumentChunkRepository.delete_by_document_id(
            db=db,
            document_id=document.id
        )

        DocumentRepository.delete(
            db=db,
            document=document
        )

        return True