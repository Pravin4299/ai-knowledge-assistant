from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.core.auth_dependencies import get_current_user
from app.services.hybrid_retrieval_service import (
    HybridRetrievalService
)

router = APIRouter(
    prefix="/documents",
    tags=["Document Search"]
)


@router.get("/search")
def search_documents(
    query: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    results = (
        HybridRetrievalService.retrieve(
            db=db,
            user_id=current_user.id,
            question=query,
            top_k=10
        )
    )

    return [
        {
            "filename": item["filename"],
            "chunk_index": item["chunk_index"],
            "chunk_text": item["chunk_text"],
            "distance": item["distance"]
        }
        for item in results
    ]