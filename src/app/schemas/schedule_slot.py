from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.schemas.user import DoctorShortSchema

class ScheduleSlotSchema(BaseModel):
    id: int

    slot_start: datetime
    slot_end: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class AvailableSlotsSchema(BaseModel):
    id: int

    slot_start: datetime
    slot_end: datetime

    doctor: DoctorShortSchema

    model_config = ConfigDict(
        from_attributes=True,
    )