from pydantic import BaseModel, EmailStr

from common.enums.user_role import UserRole

class MeSchema(BaseModel):
    id: int
    email: EmailStr
    phone: str

    first_name: str
    last_name: str
    middle_name: str | None = None

    role: UserRole
    specialization: int | None = None

    is_active: bool
    is_verified: bool