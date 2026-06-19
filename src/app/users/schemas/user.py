from pydantic import BaseModel, ConfigDict

from app.users.schemas.specialization import SpecializationShortSchema

from common.enums.user_role import UserRole

class UserShortSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str | None = None

    model_config = ConfigDict(from_attributes=True)

class DoctorShortSchema(UserShortSchema):
    specialization: SpecializationShortSchema | None


class PatientShortSchema(UserShortSchema):
    pass


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

class PatientResponseSchema(PatientCreateSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)

class DoctorResponseSchema(DoctorCreateSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)
