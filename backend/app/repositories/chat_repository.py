from sqlalchemy.orm import Session

from app.models.chat_session import ChatSession


class ChatRepository:

    @staticmethod
    def create(
        db: Session,
        session: ChatSession
    ):
        db.add(session)
        db.commit()
        db.refresh(session)

        return session
    
    @staticmethod
    def get_user_sessions(
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 20
    ):
        return (
            db.query(ChatSession)
            .filter(
                ChatSession.user_id == user_id,
                ChatSession.is_deleted == False
            )
            .order_by(
                ChatSession.updated_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    @staticmethod
    def get_user_session(
        db: Session,
        session_id: str,
        user_id: str
    ):
        return (
            db.query(ChatSession)
            .filter(
                ChatSession.id == session_id,
                ChatSession.user_id == user_id,
                ChatSession.is_deleted == False
            )
            .first()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        session_id: str
    ):
        return (
            db.query(ChatSession)
            .filter(
                ChatSession.id == session_id,
                ChatSession.is_deleted == False
            )
            .first()
        )
    
    @staticmethod
    def update(
        db: Session,
        session: ChatSession
    ):
        db.commit()
        db.refresh(session)

        return session
    
    @staticmethod
    def soft_delete(
        db: Session,
        session: ChatSession
    ):
        session.is_deleted = True

        db.commit()

        return True