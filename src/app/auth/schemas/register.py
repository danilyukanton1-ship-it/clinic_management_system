from pydantic import BaseModel, EmailStr, Field

class RegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    middle_name: str | None = Field(min_length=1, max_length=100)

    phone: str = Field(min_length=1, max_length=20)

class RegisterResponseSchema(BaseModel):
    id: int
    email: EmailStr

    first_name: str
    last_name: str

    phone: str
