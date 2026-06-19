import datetime

from pydantic import BaseModel, ConfigDict
from common.enums.appointment_status import AppointmentStatus


class AppointmentCreateSchema(BaseModel):
    patient: int
    doctor: int

    slot_id: int

    complaint: str | None = None

class AppointmentUpdateSchema(BaseModel):
    complaint: str | None = None
    status: AppointmentStatus | None = None

class AppointmentResponseSchema(BaseModel):
    id: int

    patient_id: int
    doctor_id: int

    status: AppointmentStatus
    slot_id: int

    complaint: str | None

    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)



