from datetime import datetime
from datetime import timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings
from jose import JWTError
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class Security:

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(
        plain_password: str,
        hashed_password: str
    ) -> bool:
        return pwd_context.verify(
            plain_password,
            hashed_password
        )

    @staticmethod
    def create_access_token(
        data: dict
    ) -> str:

        payload = data.copy()

        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload.update(
            {"exp": expire}
        )

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
    
    @staticmethod
    def decode_token(token: str):
        try:
            return jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM]
            )
        except JWTError:
            return None
    
    @staticmethod
    def create_refresh_token(data: dict):

        payload = data.copy()

        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

        payload.update(
            {
                "exp": expire,
                "type": "refresh"
            }
        )

        return jwt.encode(
            payload,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )