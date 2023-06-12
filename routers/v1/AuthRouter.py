from fastapi import APIRouter, Depends, Body, status, HTTPException

from schemas.AuthSchema import LoginSchema, TokenSchema
from services.UserService import UserService

AuthRouter = APIRouter(prefix="/v1/auth", tags=["auth"])


@AuthRouter.post(
    "/",
    response_model=TokenSchema,
    status_code=status.HTTP_200_OK,
)
def post(
    auth: LoginSchema = Body(),
    user_service: UserService = Depends(),
):
    try:
        user = user_service.get_by_email(email=auth.email)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user credentials"
        )
    is_validated: bool = user.validate_password(auth.hashed_password)
    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user credentials"
        )

    return user.generate_token()
