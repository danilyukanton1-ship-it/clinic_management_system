import datetime

from pydantic import BaseModel, ConfigDict
from app.enums.appointment_status import AppointmentStatus
from app.schemas.schedule_slot import ScheduleSlotSchema
from app.schemas.user import DoctorShortSchema, PatientShortSchema

class AppointmentCreateSchema(BaseModel):

    slot_id: int

    complaint: str | None = None

class AppointmentUpdateSchema(BaseModel):
    complaint: str | None = None
    status: AppointmentStatus | None = None

class AppointmentResponseSchema(BaseModel):
    id: int

    patient: PatientShortSchema
    doctor: DoctorShortSchema

    status: AppointmentStatus
    slot: ScheduleSlotSchema

    complaint: str | None

    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

