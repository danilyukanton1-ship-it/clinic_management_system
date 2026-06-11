from sqlalchemy import ForeignKey, Enum, Text, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.models import BaseModel

from app.enums.appointment_status import AppointmentStatus

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

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='RESTRICT'),
        nullable=False,
    )

    slot_id: Mapped[int] = mapped_column(
        ForeignKey('schedule_slots.id', ondelete='RESTRICT'),
        nullable=False,
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

