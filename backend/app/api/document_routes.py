from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.core.auth_dependencies import get_current_user
from app.core.dependencies import get_db
from app.repositories.document_repository import DocumentRepository
from app.schemas.document_schema import DocumentResponse
from app.services.document_service import DocumentService

from app.repositories.document_chunk_repository import (
    DocumentChunkRepository
)
from app.schemas.document_chunk_schema import (
    DocumentChunkResponse
)

from app.services.document_management_service import (
    DocumentManagementService
)
from fastapi import BackgroundTasks


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload")
def upload_document(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return DocumentService.save_file(
        db=db,
        user_id=current_user.id,
        uploaded_file=file,
        background_tasks=background_tasks
    )

@router.get(
    "",
    response_model=list[DocumentResponse]
)
def get_documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return DocumentRepository.get_user_documents(
        db=db,
        user_id=current_user.id
    )

@router.get(
    "/{document_id}/chunks",
    response_model=list[DocumentChunkResponse]
)
def get_document_chunks(
    document_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return DocumentChunkRepository.get_document_chunks(
        db=db,
        document_id=document_id
    )

@router.delete("/{document_id}")
def delete_document(
    document_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    document = DocumentRepository.get_by_id(
        db=db,
        document_id=document_id
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    DocumentManagementService.delete_document(
        db=db,
        document=document
    )

    return {
        "message": "Document deleted"
    }

@router.get("")
def get_documents(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return DocumentRepository.get_user_documents(
        db=db,
        user_id=current_user.id
    )

@router.get("/{document_id}/status")
def get_document_status(
    document_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    document = DocumentRepository.get_by_id(
        db,
        document_id
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    if document.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return {
        "status":
            document.processing_status
    }