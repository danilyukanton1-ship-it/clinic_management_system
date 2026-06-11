from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.enums.absence_reason import AbsenceReason
from app.schemas.user import DoctorShortSchema


class ScheduleAbsenceCreateSchema(BaseModel):
    doctor_id: int

    start_date: datetime
    end_date: datetime

    reason: AbsenceReason
    description: str

class ScheduleAbsenceResponseSchema(BaseModel):
    id: int

    doctor: DoctorShortSchema

    start_date: datetime
    end_date: datetime

    reason: AbsenceReason
    description: str

    model_config = ConfigDict(
        from_attributes=True,
    )