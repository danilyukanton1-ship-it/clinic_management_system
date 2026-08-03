from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, model_validator

from common.enums.absence_reason import AbsenceReason


class ScheduleAbsenceSchema(BaseModel):
    start_date: datetime = Field(
        description="Absence start date and time.",
        examples=["2026-08-10T09:00:00Z"],
    )

    end_date: datetime = Field(
        description="Absence end date and time.",
        examples=["2026-08-15T18:00:00Z"],
    )

    reason: AbsenceReason = Field(
        description="Reason for the doctor's absence.",
        examples=["vacation"],
    )

    description: str | None = Field(
        default=None,
        min_length=5,
        max_length=2000,
        description="Additional information about the absence.",
        examples=["Annual paid vacation."],
    )

    @model_validator(mode="after")
    def validate_date(self):
        if self.start_date >= self.end_date:
            raise ValueError("Start date must be before end date")
        return self


class ScheduleAbsenceResponseSchema(BaseModel):
    id: PositiveInt = Field(
        description="Schedule absence identifier.",
        examples=[1],
    )

    doctor_id: PositiveInt = Field(
        description="Doctor identifier.",
        examples=[5],
    )

    start_date: datetime = Field(
        description="Absence start date and time.",
        examples=["2026-08-10T09:00:00Z"],
    )

    end_date: datetime = Field(
        description="Absence end date and time.",
        examples=["2026-08-15T18:00:00Z"],
    )

    reason: AbsenceReason = Field(
        description="Reason for the doctor's absence.",
        examples=["vacation"],
    )

    description: str | None = Field(
        default=None,
        description="Additional information about the absence.",
        examples=["Annual paid vacation."],
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


class ScheduleAbsenceCreateSchema(ScheduleAbsenceSchema):
    doctor_id: PositiveInt = Field(
        description="Doctor identifier.",
        examples=[5],
    )


class ScheduleAbsenceUpdateSchema(ScheduleAbsenceSchema):
    pass
