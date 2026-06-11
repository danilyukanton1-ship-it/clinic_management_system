from pydantic import BaseModel, ConfigDict

from app.schemas.specialization import SpecializationShortSchema


class UserShortSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str

    model_config = ConfigDict(from_attributes=True)

class DoctorShortSchema(UserShortSchema):
    specialization: SpecializationShortSchema | None


class PatientShortSchema(UserShortSchema):
    pass