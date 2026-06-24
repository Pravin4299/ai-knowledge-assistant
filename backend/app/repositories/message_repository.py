from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage


class MessageRepository:

    @staticmethod
    def create(
        db: Session,
        message: ChatMessage
    ):
        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    @staticmethod
    def get_session_messages(
        db,
        session_id,
        skip=0,
        limit=50
    ):
        return (
            db.query(ChatMessage)
            .filter(
                ChatMessage.session_id == session_id
            )
            .order_by(
                ChatMessage.created_at.asc()
            )
            .offset(skip)
            .all()
        )
    
    @staticmethod
    def get_recent_messages(
        db: Session,
        session_id: str,
        limit: int = 20
    ):
        return (
            db.query(ChatMessage)
            .filter(
                ChatMessage.session_id == session_id
            )
            .order_by(
                ChatMessage.created_at.asc()
            )
            .limit(limit)
            .all()
        )
