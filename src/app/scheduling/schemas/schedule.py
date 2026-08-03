from datetime import time

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, model_validator

from common.enums.weekday import Weekday


class ScheduleSchema(BaseModel):
    start_time: time = Field(
        description="Working day start time.",
        examples=["09:00:00"],
    )

    end_time: time = Field(
        description="Working day end time.",
        examples=["18:00:00"],
    )

    lunch_start_time: time = Field(
        description="Lunch break start time.",
        examples=["13:00:00"],
    )

    lunch_end_time: time = Field(
        description="Lunch break end time.",
        examples=["14:00:00"],
    )

    slot_duration_minutes: PositiveInt = Field(
        ge=5,
        le=180,
        description="Duration of a single appointment slot in minutes.",
        examples=[30],
    )

    @model_validator(mode="after")
    def validate_schedule(self):
        if self.start_time >= self.end_time:
            raise ValueError("Start time must be before end time")
        if self.lunch_start_time >= self.lunch_end_time:
            raise ValueError("Lunch start time must be before lunch end time")
        if self.lunch_start_time < self.start_time:
            raise ValueError("Lunch must be within working hours")
        if self.lunch_end_time > self.end_time:
            raise ValueError("Lunch must be within working hours")
        return self


class ScheduleCreateSchema(ScheduleSchema):
    doctor_id: PositiveInt = Field(
        description="Doctor identifier.",
        examples=[5],
    )

    weekday: Weekday = Field(
        description="Day of the week for the schedule.",
        examples=["Monday"],
    )


class ScheduleResponseSchema(BaseModel):
    id: PositiveInt = Field(
        description="Schedule identifier.",
        examples=[1],
    )

    doctor_id: PositiveInt = Field(
        description="Doctor identifier.",
        examples=[5],
    )

    weekday: Weekday = Field(
        description="Day of the week for the schedule.",
        examples=["Monday"],
    )

    start_time: time = Field(
        description="Working day start time.",
        examples=["09:00:00"],
    )

    end_time: time = Field(
        description="Working day end time.",
        examples=["18:00:00"],
    )

    lunch_start_time: time = Field(
        description="Lunch break start time.",
        examples=["13:00:00"],
    )

    lunch_end_time: time = Field(
        description="Lunch break end time.",
        examples=["14:00:00"],
    )

    slot_duration_minutes: PositiveInt = Field(
        description="Duration of a single appointment slot in minutes.",
        examples=[30],
    )

    is_active: bool = Field(
        description="Indicates whether the schedule is active.",
        examples=[True],
    )

    model_config = ConfigDict(
        from_attributes=True,
    )


class ScheduleUpdateSchema(ScheduleSchema):
    pass
