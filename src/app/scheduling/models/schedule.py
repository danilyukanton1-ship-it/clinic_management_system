import datetime

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Time
from sqlalchemy.orm import Mapped, mapped_column

from common.enums.weekday import Weekday
from db import orm as orm_fields
from db.base import BaseModel


class Schedule(BaseModel):
    __tablename__ = "schedules"

    __table_args__ = (
        CheckConstraint("end_time > start_time", name="ck_schedule_end_after_start"),
        CheckConstraint(
            "lunch_end_time > lunch_start_time",
            name="ck_schedule_lunch_end_after_start",
        ),
        CheckConstraint(
            "(lunch_start_time IS NULL AND lunch_end_time IS NULL) OR"
            "(lunch_start_time IS NOT NULL AND lunch_end_time IS NOT NULL)",
            name="ck_schedule_lunch_both_null_or_both_not_null",
        ),
    )

    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    weekday: Mapped[Weekday] = mapped_column(
        Enum(Weekday, name="weekday_enums"), nullable=False
    )
    lunch_start_time: Mapped[datetime.time] = mapped_column(Time, nullable=True)
    lunch_end_time: Mapped[datetime.time] = mapped_column(Time, nullable=True)
    start_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    end_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)

    slot_duration_minutes: Mapped[orm_fields.not_nullable_int]
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
