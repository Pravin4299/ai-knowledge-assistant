from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import LoginRequest
from app.schemas.auth_schema import TokenResponse
from app.schemas.user_schema import UserCreate
from app.schemas.user_schema import UserResponse
from app.services.auth_service import AuthService

from app.schemas.auth_schema import RefreshTokenRequest
from app.core.security import Security

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):

    existing_email = UserRepository.get_by_email(
        db,
        user_data.email
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    existing_username = UserRepository.get_by_username(
        db,
        user_data.username
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    return AuthService.create_user(
        db,
        user_data
    )


@router.post(
    "/login",
    response_model=TokenResponse
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    return AuthService.login(
        db=db,
        email=request.email,
        password=request.password
    )

@router.post("/refresh")
def refresh_token(
    request: RefreshTokenRequest
):
    payload = Security.decode_token(
        request.refresh_token
    )

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

    user_id = payload["sub"]

    access_token = Security.create_access_token(
        {
            "sub": user_id
        }
    )

    return {
        "access_token": access_token
    }