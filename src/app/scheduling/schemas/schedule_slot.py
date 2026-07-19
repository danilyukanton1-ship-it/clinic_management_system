from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator

from common.enums.slot_status import SlotStatus


class ScheduleSlotSchema(BaseModel):
    slot_start: datetime
    slot_end: datetime
    status: SlotStatus

    @model_validator(mode="after")
    def validate_slot_time(self):
        if self.slot_end <= self.slot_start:
            raise ValueError("slot_end must be greater than slot_start")
        return self

class ScheduleSlotResponseSchema(ScheduleSlotSchema):
    id: int
    doctor_id: int

    model_config = ConfigDict(
        from_attributes=True
    )

class ScheduleSlotCreateSchema(ScheduleSlotSchema):
    schedule_id: int
    doctor_id: int


class ScheduleSlotUpdateSchema(ScheduleSlotSchema):
    pass


