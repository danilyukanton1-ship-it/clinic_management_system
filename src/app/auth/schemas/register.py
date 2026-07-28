from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from app.users.schemas.user import UserCreateSchema


class RegisterSchema(UserCreateSchema):
    pass


class VerifyEmailSchema(BaseModel):
    email: EmailStr
    verification_code: str = Field(
        min_length=6,
        max_length=6,
        pattern=r"^\d{6}$",
    )


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


class ResetPasswordSchema(VerifyEmailSchema):
    password: str = Field(
        min_length=8,
        max_length=128,
    )
