from pydantic import BaseModel, EmailStr, Field


class LoginSchema(BaseModel):
    email: EmailStr = Field(
        description="User email address.",
        examples=["john.doe@example.com"],
    )

    password: str = Field(
        min_length=8,
        max_length=128,
        description="User account password.",
        examples=["SecurePassword123!"],
    )
