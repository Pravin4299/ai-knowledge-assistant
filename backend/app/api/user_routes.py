from fastapi import APIRouter
from fastapi import Depends

from app.core.auth_dependencies import get_current_user
from app.schemas.user_schema import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/me",
    response_model=UserResponse
)
def get_profile(
    current_user=Depends(get_current_user)
):
    return current_user