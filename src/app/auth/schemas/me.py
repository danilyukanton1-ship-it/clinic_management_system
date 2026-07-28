from pydantic import BaseModel, EmailStr, PositiveInt, ConfigDict

from common.enums.user_role import UserRole


class MeSchema(BaseModel):
    id: PositiveInt
    email: EmailStr
    phone: str

    first_name: str
    last_name: str
    middle_name: str | None = None

    role: UserRole
    specialization: PositiveInt | None = None

    is_active: bool
    is_verified: bool

    model_config = ConfigDict(
        from_attributes=True,
    )
