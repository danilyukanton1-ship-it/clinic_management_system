import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic import PositiveInt
from common.enums.appointment_status import AppointmentStatus


class AppointmentCreateSchema(BaseModel):
    patient_id: PositiveInt
    doctor_id: PositiveInt

    slot_id: PositiveInt

    complaint: str | None = Field(
        default=None,
        min_length=3,
        max_length=1000,
    )

class AppointmentUpdateSchema(BaseModel):
    complaint: str | None = Field(
        default=None,
        min_length=3,
        max_length=1000,
    )
    status: AppointmentStatus | None = None

class AppointmentResponseSchema(BaseModel):
    id: PositiveInt

    patient_id: PositiveInt
    doctor_id: PositiveInt

    status: AppointmentStatus
    slot_id: PositiveInt

    complaint: str | None = None

    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)



