import bcrypt
import jwt
from sqlalchemy import (
    Column,
    Integer,
    PrimaryKeyConstraint,
    String,
    UniqueConstraint,
    LargeBinary,
)

from models.BaseModel import EntityMeta
from configs.Environment import get_environment_variables


env = get_environment_variables()


class User(EntityMeta):
    __tablename__ = "users"

    id = Column(Integer)
    name = Column(String(16), nullable=False)
    last_name = Column(String(16), nullable=False)
    email = Column(String(225), unique=True, nullable=False)
    hashed_password = Column(LargeBinary, nullable=False)

    UniqueConstraint("email", name="uq_user_email")
    PrimaryKeyConstraint(id, name="pk_user_id")

    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
            "last_name": self.last_name.__str__(),
            "email": self.email.__str__(),
        }

    @staticmethod
    def hash_password(password) -> bytes:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, password) -> bool:
        return bcrypt.checkpw(password.encode(), self.hashed_password)

    def generate_token(self) -> dict:
        return {
            "access_token": jwt.encode(
                {
                    "api_key": env.API_KEY,
                    "email": self.email,
                },
                env.SECRET_KEY,
                algorithm=env.ALGORITHM,
            )
        }
