import os
import uuid

from app.models.document import Document
from app.repositories.document_repository import DocumentRepository
from app.constants.file_constants import ALLOWED_EXTENSIONS

from fastapi import HTTPException
from app.tasks.document_tasks import (process_document_background)
class DocumentService:

    STORAGE_DIR = "storage"

    @staticmethod
    def save_file(
        db,
        user_id: str,
        uploaded_file,
        background_tasks
    ):

        extension = uploaded_file.filename.split(".")[-1].lower()
        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type"
            )

        user_dir = os.path.join(
            DocumentService.STORAGE_DIR,
            user_id
        )

        os.makedirs(
            user_dir,
            exist_ok=True
        )

        file_id = str(uuid.uuid4())

        file_path = os.path.join(
            user_dir,
            f"{file_id}_{uploaded_file.filename}"
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.file.read())

        document = Document(
            user_id=user_id,
            filename=uploaded_file.filename,
            file_type=uploaded_file.filename.split(".")[-1],
            file_size=os.path.getsize(file_path),
            file_path=file_path,
            processing_status="pending"
        )
    
        document = DocumentRepository.create(
            db=db,
            document=document
        )

        background_tasks.add_task(
            process_document_background,
            document.id
        )
        return {
            "document_id": document.id,
            "filename": document.filename,
            "status": "pending"
        }
        # DocumentProcessingService.process_document(
        #     db=db,
        #     document=document
        # )

        # return document
    
    @staticmethod
    def get_user_documents(
        db,
        user_id: str
    ):
        return DocumentRepository.get_user_documents(
            db=db,
            user_id=user_id
        )