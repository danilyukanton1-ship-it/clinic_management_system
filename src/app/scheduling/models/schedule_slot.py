from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.enums.slot_status import SlotStatus
from db import orm as orm_fields
from db.base import BaseModel

if TYPE_CHECKING:
    from app.appointments.models.appointment import Appointment


class ScheduleSlot(BaseModel):
    __tablename__ = "schedule_slots"

    __table_args__ = (
        UniqueConstraint(
            "doctor_id",
            "slot_start",
            name="uq_doctor_slot_start",
        ),
        CheckConstraint(
            "slot_end > slot_start",
            name="ck_slot_end_after_start",
        ),
    )

    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("schedules.id", ondelete="RESTRICT"), nullable=False
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )

    appointment: Mapped["Appointment"] = relationship(
        "Appointment",
        back_populates="slot",
        uselist=False,
    )

    slot_start: Mapped[orm_fields.datetime_column]
    slot_end: Mapped[orm_fields.datetime_column]

    status: Mapped[SlotStatus] = mapped_column(
        Enum(SlotStatus, name="slot_status"), nullable=False, default=SlotStatus.FREE
    )
