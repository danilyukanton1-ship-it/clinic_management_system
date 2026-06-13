from datetime import time

from pydantic import BaseModel, ConfigDict

from app.enums.weekday import Weekday
from app.schemas.user import DoctorShortSchema

class ScheduleCreateSchema(BaseModel):

    doctor_id: int

    weekday: Weekday

    start_time: time
    end_time: time

    slot_duration_minutes: int


class ScheduleResponseSchema(BaseModel):
    id: int

    doctor: DoctorShortSchema

    weekday: Weekday
    start_time: time
    end_time: time

    slot_duration_minutes: int

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )

class ScheduleUpdateSchema(BaseModel):
    doctor_id: int

    weekday: Weekday

    start_time: time
    end_time: time

    slot_duration_minutes: int

    model_config = ConfigDict(
        from_attributes=True,
    )