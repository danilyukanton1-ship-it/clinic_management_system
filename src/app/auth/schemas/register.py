from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from app.users.schemas.user import UserCreateSchema


class RegisterSchema(UserCreateSchema):
    pass


class VerifyEmailSchema(BaseModel):
    email: EmailStr = Field(
        description="User email address.",
        examples=["john.doe@example.com"],
    )

    verification_code: str = Field(
        min_length=6,
        max_length=6,
        pattern=r"^\d{6}$",
        description="Six-digit email verification code.",
        examples=["123456"],
    )


class ForgotPasswordSchema(BaseModel):
    email: EmailStr = Field(
        description="User email address.",
        examples=["john.doe@example.com"],
    )


class ResetPasswordSchema(VerifyEmailSchema):
    password: str = Field(
        min_length=8,
        max_length=128,
        description="New account password.",
        examples=["SecurePassword123!"],
    )
