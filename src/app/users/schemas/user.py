from pydantic import BaseModel, ConfigDict

from common.enums.user_role import UserRole

class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str | None = None
    email: str
    phone: str | None = None
    role: UserRole

    model_config = ConfigDict(from_attributes=True)

class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None
    phone: str | None = None
    email: str
    password_hash: str
    role: UserRole

class PatientCreateSchema(UserCreateSchema):
    pass

class DoctorCreateSchema(UserCreateSchema):
    specialization_id: int
    phone: str


class PatientResponseSchema(UserResponseSchema):

    model_config = ConfigDict(from_attributes=True)

class DoctorResponseSchema(UserResponseSchema):
    specialization_id: int
    model_config = ConfigDict(from_attributes=True)

class UserUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None
    phone: str | None = None
    email: str
    is_active: bool


class PatientUpdateSchema(UserUpdateSchema):
    pass


class DoctorUpdateSchema(UserUpdateSchema):
    specialization_id: int