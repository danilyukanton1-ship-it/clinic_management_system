from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, model_validator

from common.enums.slot_status import SlotStatus


class ScheduleSlotSchema(BaseModel):
    slot_start: datetime = Field(
        description="Schedule slot start date and time.",
        examples=["2026-08-15T09:00:00Z"],
    )

    slot_end: datetime = Field(
        description="Schedule slot end date and time.",
        examples=["2026-08-15T09:30:00Z"],
    )

    status: SlotStatus = Field(
        description="Current schedule slot status.",
        examples=["free"],
    )

    @model_validator(mode="after")
    def validate_slot_time(self):
        if self.slot_end <= self.slot_start:
            raise ValueError("Slot end time must be after slot start time")
        return self


class ScheduleSlotResponseSchema(BaseModel):
    id: PositiveInt = Field(
        description="Schedule slot identifier.",
        examples=[1],
    )

    doctor_id: PositiveInt = Field(
        description="Doctor identifier.",
        examples=[5],
    )

    slot_start: datetime = Field(
        description="Schedule slot start date and time.",
        examples=["2026-08-15T09:00:00Z"],
    )

    slot_end: datetime = Field(
        description="Schedule slot end date and time.",
        examples=["2026-08-15T09:30:00Z"],
    )

    status: SlotStatus = Field(
        description="Current schedule slot status.",
        examples=["free"],
    )

    model_config = ConfigDict(from_attributes=True)


class ScheduleSlotCreateSchema(ScheduleSlotSchema):
    schedule_id: PositiveInt = Field(
        description="Schedule identifier.",
        examples=[10],
    )

    doctor_id: PositiveInt = Field(
        description="Doctor identifier.",
        examples=[5],
    )


class ScheduleSlotUpdateSchema(ScheduleSlotSchema):
    pass


class ScheduleSlotBulkCreateSchema(BaseModel):
    start_date: date = Field(
        description="Start date for schedule slot generation.",
        examples=["2026-08-15"],
    )

    end_date: date = Field(
        description="End date for schedule slot generation.",
        examples=["2026-08-31"],
    )

    doctor_id: PositiveInt = Field(
        description="Doctor identifier.",
        examples=[5],
    )
