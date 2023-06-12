from typing import Optional, Type

from fastapi import Depends
from sqlalchemy.orm import Session

from configs.Database import (
    get_db_connection,
)
from models.UserModel import User


class UserRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)) -> None:
        self.db = db

    def list(
        self,
        limit: Optional[int],
        start: Optional[int],
    ) -> list[Type[User]]:
        query = self.db.query(User)

        return query.offset(start).limit(limit).all()

    def get(self, user: User) -> Type[User] | None:
        return self.db.get(User, user.id)

    def get_by_email(self, email: str) -> Type[User]:
        return self.db.query(User).filter(User.email == email).one()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, id: int, user: User) -> User:
        user.id = id
        self.db.merge(user)
        self.db.commit()
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
        self.db.flush()
