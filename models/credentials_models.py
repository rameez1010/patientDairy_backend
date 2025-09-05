from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    token: str


class Credentials(BaseModel):
    password: str
    email: EmailStr


class PasswordUpdate(BaseModel):
    current_password: str = Field(..., min_length=3, description="Current password")
    new_password: str = Field(..., min_length=6, description="New password")
