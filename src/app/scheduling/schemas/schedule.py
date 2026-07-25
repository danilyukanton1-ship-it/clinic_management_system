from datetime import time

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, model_validator

from common.enums.weekday import Weekday

class ScheduleSchema(BaseModel):
    start_time: time
    end_time: time
    lunch_start_time: time
    lunch_end_time: time
    slot_duration_minutes: PositiveInt = Field(
        ge=5,
        le=180
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
    doctor_id: PositiveInt
    weekday: Weekday


class ScheduleResponseSchema(BaseModel):
    id: PositiveInt

    doctor_id: PositiveInt

    weekday: Weekday
    start_time: time
    end_time: time
    lunch_start_time: time
    lunch_end_time: time

    slot_duration_minutes: PositiveInt

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )

class ScheduleUpdateSchema(ScheduleSchema):
    pass