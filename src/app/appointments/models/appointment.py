from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, Enum, Text, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import BaseModel

from common.enums.appointment_status import AppointmentStatus
if TYPE_CHECKING:
    from app.users.models.user import User
    from app.scheduling.models.schedule_slot import ScheduleSlot


class Appointment(BaseModel):
    __tablename__ = 'appointments'

    __table_args__ = (
        UniqueConstraint(
            'slot_id',
            name='uq_appointment_slot'
        ),
        CheckConstraint(
            'doctor_id <> patient_id',
            name='ck_doctor_not_patient'
        )
    )

    patient_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='RESTRICT'),
        nullable=False,
    )

    patient: Mapped["User"] = relationship(
        'User',
        foreign_keys=[patient_id],
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='RESTRICT'),
        nullable=False,
    )

    doctor: Mapped["User"] = relationship(
        'User',
        foreign_keys=[doctor_id],
    )

    slot_id: Mapped[int] = mapped_column(
        ForeignKey('schedule_slots.id', ondelete='RESTRICT'),
        nullable=False,
    )

    slot: Mapped["ScheduleSlot"] = relationship(
        'ScheduleSlot',
        foreign_keys=[slot_id],
    )

    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(
            AppointmentStatus,
            name='appointment_status'
        ),
        nullable=False,
        default=AppointmentStatus.SCHEDULED
    )

    complaint: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

