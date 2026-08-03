from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, model_validator

from common.enums.absence_reason import AbsenceReason


class ScheduleAbsenceSchema(BaseModel):
    start_date: datetime
    end_date: datetime

    reason: AbsenceReason
    description: str | None = Field(default=None, min_length=5, max_length=2000)

    @model_validator(mode="after")
    def validate_date(self):
        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date")
        return self


class ScheduleAbsenceResponseSchema(BaseModel):
    id: PositiveInt
    doctor_id: PositiveInt
    start_date: datetime
    end_date: datetime
    reason: AbsenceReason
    description: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )


class ScheduleAbsenceCreateSchema(ScheduleAbsenceSchema):
    doctor_id: PositiveInt


class ScheduleAbsenceUpdateSchema(ScheduleAbsenceSchema):
    pass
