from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user
from app.core.dependencies import get_db
from app.repositories.message_repository import MessageRepository
from app.schemas.message_schema import CreateMessageRequest
from app.schemas.message_schema import MessageResponse
from app.services.chat_service import ChatService
from app.services.message_service import MessageService

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

@router.post(
    "",
    response_model=MessageResponse
)
def create_message(
    request: CreateMessageRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    session = ChatService.validate_session_owner(
        db=db,
        session_id=request.session_id,
        user_id=current_user.id
    )

    return MessageService.create_user_message(
        db=db,
        session=session,
        content=request.content
    )

@router.get(
    "/{session_id}",
    response_model=list[MessageResponse]
)
def get_messages(
    session_id: str,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    session = ChatService.validate_session_owner(
        db=db,
        session_id=session_id,
        user_id=current_user.id
    )

    return MessageRepository.get_session_messages(
        db=db,
        session_id=session.id
    )