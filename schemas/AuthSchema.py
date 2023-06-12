from pydantic import BaseModel, EmailStr, Field


class LoginSchema(BaseModel):
    email: EmailStr
    hashed_password: str = Field(alias="password")


class TokenSchema(BaseModel):
    access_token: str
