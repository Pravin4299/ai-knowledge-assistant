from app.models.chat_session import ChatSession
from app.repositories.chat_repository import ChatRepository

from fastapi import HTTPException
from fastapi import status

class ChatService:

    @staticmethod
    def create_session(
        db,
        user_id: str,
        title: str | None
    ):

        session = ChatSession(
            user_id=user_id,
            title=title or "New Chat"
        )

        return ChatRepository.create(
            db=db,
            session=session
        )
    
    @staticmethod
    def validate_session_owner(
        db,
        session_id: str,
        user_id: str
    ):
        session = ChatRepository.get_user_session(
            db=db,
            session_id=session_id,
            user_id=user_id
        )

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )

        return session

    @staticmethod
    def rename_session(
        db,
        session,
        title: str
    ):
        session.title = title

        return ChatRepository.update(
            db=db,
            session=session
        )