from datetime import datetime

from pydantic import BaseModel, ConfigDict

from common.enums.absence_reason import AbsenceReason



class ScheduleAbsenceSchema(BaseModel):

    start_date: datetime
    end_date: datetime

    reason: AbsenceReason
    description: str | None

class ScheduleAbsenceResponseSchema(ScheduleAbsenceSchema):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )

class ScheduleAbsenceCreateSchema(ScheduleAbsenceSchema):
    doctor_id: int

class ScheduleAbsenceUpdateSchema(ScheduleAbsenceSchema):
    pass