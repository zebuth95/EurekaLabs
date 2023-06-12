from typing import Optional, Type

from fastapi import Depends
from models.UserModel import User

from repositories.UserRepository import UserRepository
from schemas.UserSchema import UserSchema


class UserService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository = Depends()) -> None:
        self.user_repository = user_repository

    def create(self, user_body: UserSchema) -> User:
        return self.user_repository.create(
            User(
                name=user_body.name,
                last_name=user_body.last_name,
                email=user_body.email,
                hashed_password=user_body.hashed_password,
            )
        )

    def delete(self, user_id: int) -> None:
        return self.user_repository.delete(User(id=user_id))

    def get(self, user_id: int) -> Type[User] | None:
        return self.user_repository.get(User(id=user_id))

    def get_by_email(self, email: str) -> Type[User] | None:
        return self.user_repository.get_by_email(email)

    def list(
        self,
        page_size: Optional[int] = 100,
        start_index: Optional[int] = 0,
    ) -> list[Type[User]]:
        return self.user_repository.list(page_size, start_index)

    def update(self, user_id: int, user_body: UserSchema) -> User:
        return self.user_repository.update(user_id, User(name=user_body.name))
