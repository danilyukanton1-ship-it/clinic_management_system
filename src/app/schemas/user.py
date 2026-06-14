from pydantic import BaseModel, ConfigDict

from app.schemas.specialization import SpecializationShortSchema

from app.enums.user_role import UserRole

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
    phone_number: str | None = None
    email: str
    password: str
    role: UserRole

class PatientCreateSchema(UserCreateSchema):
    pass

class DoctorCreateSchema(UserCreateSchema):
    specialization_id: int
    phone_number: str

class PatientResponseSchema(PatientCreateSchema):
    model_config = ConfigDict(from_attributes=True)

class DoctorResponseSchema(DoctorCreateSchema):
    model_config = ConfigDict(from_attributes=True)
