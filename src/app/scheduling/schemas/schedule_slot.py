from datetime import datetime
from pydantic import BaseModel, ConfigDict, model_validator, PositiveInt

from common.enums.slot_status import SlotStatus


class ScheduleSlotSchema(BaseModel):
    slot_start: datetime
    slot_end: datetime
    status: SlotStatus

    @model_validator(mode="after")
    def validate_slot_time(self):
        if self.slot_end <= self.slot_start:
            raise ValueError("Slot end time must be after slot start time")
        return self

class ScheduleSlotResponseSchema(BaseModel):
    id: PositiveInt
    doctor_id: PositiveInt
    slot_start: datetime
    slot_end: datetime
    status: SlotStatus

    model_config = ConfigDict(
        from_attributes=True
    )

class ScheduleSlotCreateSchema(ScheduleSlotSchema):
    schedule_id: PositiveInt
    doctor_id: PositiveInt


class ScheduleSlotUpdateSchema(ScheduleSlotSchema):
    pass


