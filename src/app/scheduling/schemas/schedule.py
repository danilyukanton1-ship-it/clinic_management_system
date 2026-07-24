from datetime import time

from pydantic import BaseModel, ConfigDict

from common.enums.weekday import Weekday


class ScheduleCreateSchema(BaseModel):

    doctor_id: int

    weekday: Weekday

    start_time: time
    end_time: time
    lunch_start_time: time
    lunch_end_time: time
    slot_duration_minutes: int


class ScheduleResponseSchema(BaseModel):
    id: int

    doctor_id: int

    weekday: Weekday
    start_time: time
    end_time: time
    lunch_start_time: time
    lunch_end_time: time

    slot_duration_minutes: int

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )

class ScheduleUpdateSchema(BaseModel):


    start_time: time
    end_time: time
    lunch_start_time: time
    lunch_end_time: time

    slot_duration_minutes: int

    model_config = ConfigDict(
        from_attributes=True,
    )