from pydantic import BaseModel, Field, EmailStr, validator


class BaseUserSchema(BaseModel):
    name: str
    last_name: str
    email: EmailStr


class UserPostRequestSchema(BaseUserSchema):
    hashed_password: str = Field(alias="password")

    @validator("hashed_password")
    @classmethod
    def hashed_password_age(cls, value):
        if len(value) < 8:
            raise ValueError("password must contain more than 8 characters ")
        return value


class UserSchema(BaseUserSchema):
    id: int
