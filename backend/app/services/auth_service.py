from sqlalchemy.orm import Session

from app.core.security import Security
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate


from fastapi import HTTPException
from fastapi import status
from app.repositories.user_repository import UserRepository


class AuthService:

    @staticmethod
    def create_user(
        db: Session,
        user_data: UserCreate
    ):

        hashed_password = Security.hash_password(
            user_data.password
        )

        user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )

        return UserRepository.create(
            db=db,
            user=user
        )
    
    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str
    ):

        user = UserRepository.get_by_email(
            db=db,
            email=email
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )

        if not Security.verify_password(
            password,
            user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials"
            )
    
        access_token = Security.create_access_token(
            {
                "sub": user.id
            }
        )

        refresh_token = Security.create_refresh_token(
            {
                "sub": user.id
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }