from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    PositiveInt,
    field_validator,
)

from common.enums.user_role import UserRole


class UserSchema(BaseModel):
    first_name: str = Field(
        min_length=1,
        max_length=100,
    )
    last_name: str = Field(
        min_length=1,
        max_length=100,
    )
    middle_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    email: EmailStr
    phone: str | None = Field(
        default=None,
        pattern=r"^\+?[1-9]\d{6,14}$",
    )

    @field_validator("first_name", "last_name", mode="before")
    @classmethod
    def validate_required_name(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be empty.")

        if any(char.isdigit() for char in value):
            raise ValueError("Field cannot contain digits.")

        return value

    @field_validator("middle_name", mode="before")
    @classmethod
    def validate_middle_name(cls, value):
        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        if any(char.isdigit() for char in value):
            raise ValueError("Field cannot contain digits.")

        return value

    @field_validator("phone", mode="before")
    @classmethod
    def empty_phone_to_none(cls, value):
        if isinstance(value, str) and not value.strip():
            return None
        return value


class UserResponseSchema(BaseModel):
    id: PositiveInt
    first_name: str
    last_name: str
    middle_name: str | None = None
    email: EmailStr
    phone: str | None = None
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserCreateSchema(UserSchema):
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class DoctorCreateSchema(UserCreateSchema):
    specialization_id: PositiveInt


class AdminCreateSchema(UserCreateSchema):
    pass


class PatientResponseSchema(UserResponseSchema):
    pass


class DoctorResponseSchema(UserResponseSchema):
    specialization_id: PositiveInt


class AdminResponseSchema(UserResponseSchema):
    pass


class UserUpdateSchema(UserSchema):
    pass


class PatientUpdateSchema(UserUpdateSchema):
    pass


class AdminUpdateSchema(UserUpdateSchema):
    pass


class DoctorUpdateSchema(UserUpdateSchema):
    specialization_id: PositiveInt
