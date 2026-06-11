from sqlalchemy import Enum, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core import orm as orm_fields
from core.models import BaseModel

from app.enums.absence_reason import AbsenceReason


class ScheduleAbsence(BaseModel):
    __tablename__ = 'schedule_absences'

    __table_args__ = (
        CheckConstraint(
            'end_time > start_time',
            name='ck_schedule_absence_end_after_start'
        ),
    )

    doctor_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    start_date: Mapped[orm_fields.datetime_column]
    end_date: Mapped[orm_fields.datetime_column]

    reason: Mapped[AbsenceReason] = mapped_column(
        Enum(
            AbsenceReason,
            name='absence_reason'
        ),
        nullable=False
    )

    description: Mapped[orm_fields.text_column]
