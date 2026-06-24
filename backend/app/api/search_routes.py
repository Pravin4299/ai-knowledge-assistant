from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.services.retrieval_service import (
    RetrievalService
)

from app.services.rag_service import (
    RAGService
)
from app.core.auth_dependencies import get_current_user
router = APIRouter(
    prefix="/search",
    tags=["Search"]
)

@router.get("")
def search(
    query: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    results = RetrievalService.retrieve(
        db=db,
        user_id=current_user.id,
        question=query,
        top_k=5
    )
    print("results=========",results)
    return results

@router.get("/rag-test")
def rag_test(
    query: str,
    db: Session = Depends(get_db)
):
    return {
        "answer": RAGService.answer(
            db=db,
            question=query
        )
    }