import datetime

from pydantic import BaseModel, ConfigDict
from app.enums.appointment_status import AppointmentStatus
from app.schemas.user import DoctorShortSchema, UserShortSchema

class AppointmentCreateSchema(BaseModel):

    slot_id: int

    complaint: str | None = None

class AppointmentUpdateSchema(BaseModel):
    slot_id: int
    complaint: str | None = None

class AppointmentResponseSchema(BaseModel):
    id: int

    patient: UserShortSchema
    doctor: DoctorShortSchema

    status: AppointmentStatus

    complaint: str | None

    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)