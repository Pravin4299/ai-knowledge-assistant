from datetime import datetime

from app.constants.message_role import MessageRole
from app.models.chat_message import ChatMessage
from app.repositories.chat_repository import ChatRepository
from app.repositories.message_repository import MessageRepository
from app.utils.token_utils import count_tokens

class MessageService:

    @staticmethod
    def create_user_message(
        db,
        session,
        content: str
    ):
        
        message = ChatMessage(
            session_id=session.id,
            role=MessageRole.USER.value,
            content=content,
            token_count=count_tokens(content)
        )

        saved_message = MessageRepository.create(
            db=db,
            message=message
        )
        
        session.message_count += 1
        session.last_message_at = datetime.utcnow()

        ChatRepository.update(
            db=db,
            session=session
        )

        return saved_message

    @staticmethod
    def create_assistant_message(
        db,
        session,
        content: str
    ):

        message = ChatMessage(
            session_id=session.id,
            role=MessageRole.ASSISTANT.value,
            content=content,
            token_count=count_tokens(content)
        )

        saved_message = MessageRepository.create(
            db=db,
            message=message
        )

        session.message_count += 1
        session.last_message_at = datetime.utcnow()

        ChatRepository.update(
            db=db,
            session=session
        )

        return saved_message