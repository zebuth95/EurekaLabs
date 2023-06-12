from typing import List, Optional

from fastapi import APIRouter, Depends, status, Body, HTTPException, Request

from configs.Auth import oauth2_scheme
from configs.Limiter import limiter
from schemas.UserSchema import UserPostRequestSchema, UserSchema
from services.UserService import UserService
from models.UserModel import User

UserRouter = APIRouter(prefix="/v1/users", tags=["user"])


@UserRouter.get("/", response_model=List[UserSchema])
def index(
    request: Request,
    page_size: Optional[int] = 100,
    start_index: Optional[int] = 0,
    user_service: UserService = Depends(),
    token: str = Depends(oauth2_scheme),
):
    return [user.normalize() for user in user_service.list(page_size, start_index)]


@UserRouter.get("/{id}", response_model=UserSchema)
@limiter.limit("10/minute")
def get(
    request: Request,
    id: int,
    user_service: UserService = Depends(),
    token: str = Depends(oauth2_scheme),
):
    try:
        return user_service.get(id).normalize()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@UserRouter.post(
    "/",
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("10/minute")
def create(
    request: Request,
    user: UserPostRequestSchema = Body(),
    user_service: UserService = Depends(),
):
    try:
        user.hashed_password = User.hash_password(user.hashed_password)
        return user_service.create(user).normalize()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user params"
        )
