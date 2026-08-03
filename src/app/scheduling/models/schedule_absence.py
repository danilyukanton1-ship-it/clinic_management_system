from sqlalchemy import CheckConstraint, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from common.enums.absence_reason import AbsenceReason
from db import orm as orm_fields
from db.base import BaseModel


class ScheduleAbsence(BaseModel):
    __tablename__ = "schedule_absences"

    __table_args__ = (
        CheckConstraint(
            "end_date > start_date", name="ck_schedule_absence_end_after_start"
        ),
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )

    start_date: Mapped[orm_fields.datetime_column]
    end_date: Mapped[orm_fields.datetime_column]

    reason: Mapped[AbsenceReason] = mapped_column(
        Enum(AbsenceReason, name="absence_reason"), nullable=False
    )

    description: Mapped[orm_fields.nullable_text_column]
