from sqlalchemy import ForeignKey, Enum, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import mapped_column, Mapped

from core import orm as orm_fields
from core.models import BaseModel

from app.enums.slot_status import SlotStatus


class ScheduleSlot(BaseModel):
    __tablename__ = 'schedule_slots'

    __table_args__ = (
        UniqueConstraint(
            'doctor_id',
            'slot_start',
            name='uq_doctor_slot_start',
        ),
        CheckConstraint(
            'slot_end > slot_start',
            name='ck_slot_end_after_start',
        )
    )

    schedule_id: Mapped[int] = mapped_column(ForeignKey('schedules.id'), nullable=False)
    doctor_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    slot_start: Mapped[orm_fields.datetime_column]
    slot_end: Mapped[orm_fields.datetime_column]

    status: Mapped[SlotStatus] = mapped_column(
        Enum(SlotStatus, name='slot_status'),
        nullable=False,
        default=SlotStatus.FREE
    )
