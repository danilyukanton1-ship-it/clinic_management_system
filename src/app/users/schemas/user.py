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
    phone: str
    email: str
    password: str

class DoctorCreateSchema(UserCreateSchema):
    specialization_id: int

class AdminCreateSchema(UserCreateSchema):
    pass


class PatientResponseSchema(UserResponseSchema):

    model_config = ConfigDict(from_attributes=True)

class DoctorResponseSchema(UserResponseSchema):
    specialization_id: int
    model_config = ConfigDict(from_attributes=True)

class AdminResponseSchema(UserResponseSchema):
    model_config = ConfigDict(from_attributes=True)

class UserUpdateSchema(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None = None
    phone: str | None = None
    email: str


class PatientUpdateSchema(UserUpdateSchema):
    pass

class AdminUpdateSchema(UserUpdateSchema):
    pass

class DoctorUpdateSchema(UserUpdateSchema):
    specialization_id: int