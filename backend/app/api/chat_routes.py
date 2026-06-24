from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user
from app.core.dependencies import get_db
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat_schema import ChatSessionCreate
from app.schemas.chat_schema import ChatSessionResponse
from app.services.chat_service import ChatService

from app.schemas.chat_schema import RenameSessionRequest
from app.schemas.chat_schema import MessageResponse

from app.schemas.chat_completion_schema import ChatRequest
from app.schemas.chat_completion_schema import ChatResponse
from app.services.ai_chat_service import AIChatService
from fastapi.responses import StreamingResponse
from app.services.stream_chat_service import StreamChatService
from app.services.rag_chat_service import (
    RAGChatService
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

@router.post(
    "/sessions",
    response_model=ChatSessionResponse
)
def create_session(
    request: ChatSessionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return ChatService.create_session(
        db=db,
        user_id=current_user.id,
        title=request.title
    )

@router.get(
    "/sessions",
    response_model=list[ChatSessionResponse]
)
def get_sessions(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return ChatRepository.get_user_sessions(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit
    )

@router.get(
    "/sessions/{session_id}",
    response_model=ChatSessionResponse
)
def get_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    return ChatService.validate_session_owner(
        db=db,
        session_id=session_id,
        user_id=current_user.id
    )

@router.patch(
    "/sessions/{session_id}",
    response_model=ChatSessionResponse
)
def rename_session(
    session_id: str,
    request: RenameSessionRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    session = ChatService.validate_session_owner(
        db=db,
        session_id=session_id,
        user_id=current_user.id
    )

    return ChatService.rename_session(
        db=db,
        session=session,
        title=request.title
    )

@router.delete(
    "/sessions/{session_id}",
    response_model=MessageResponse
)
def delete_session(
    session_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    session = ChatService.validate_session_owner(
        db=db,
        session_id=session_id,
        user_id=current_user.id
    )

    ChatRepository.soft_delete(
        db=db,
        session=session
    )

    return {
        "success": True,
        "message": "Session deleted successfully"
    }

@router.post(
    "/message",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    session = ChatService.validate_session_owner(
        db=db,
        session_id=request.session_id,
        user_id=current_user.id
    )

    if request.is_rag:

        answer = RAGChatService.chat(
            db=db,
            session=session,
            question=request.question,
            user_id=current_user.id
        )
    else:

        answer = AIChatService.chat(
            db=db,
            session=session,
            question=request.question
        )
    # answer = AIChatService.chat(
    #     db=db,
    #     session=session,
    #     question=request.question
    # )

    return answer


@router.post("/message/stream")
def stream_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    session = ChatService.validate_session_owner(
        db=db,
        session_id=request.session_id,
        user_id=current_user.id
    )

    if request.is_rag:

        answer = RAGChatService.stream_chat(
            db=db,
            session=session,
            question=request.question,
            user_id=current_user.id
        )
    else:

        answer = AIChatService.stream_chat(
            db=db,
            session=session,
            question=request.question
        )

    # generator = StreamChatService.stream_chat(
    #     db=db,
    #     session=session,
    #     question=request.question
    # )

    return StreamingResponse(
        answer,
        media_type="text/event-stream"
    )
