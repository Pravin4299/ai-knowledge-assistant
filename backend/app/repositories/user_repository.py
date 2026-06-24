from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ):
        return (
            db.query(User)
            .filter(User.email == email,User.is_deleted == False)
            .first()
        )

    @staticmethod
    def get_by_username(
        db: Session,
        username: str
    ):
        return (
            db.query(User)
            .filter(User.username == username,User.is_deleted == False)
            .first()
        )

    @staticmethod
    def create(
        db: Session,
        user: User
    ):
        db.add(user)
        db.commit()
        db.refresh(user)

        return user
    
    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )