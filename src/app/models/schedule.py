import datetime

from sqlalchemy import ForeignKey, Time, Enum, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.models import BaseModel
from core import orm as orm_fields

from app.enums.weekday import Weekday

class Schedule(BaseModel):
    __tablename__ = 'schedules'

    __table_args__ = (
        CheckConstraint(
            'end_time > start_time',
            name='ck_schedule_end_after_start'
        ),
    )

    doctor_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    weekday: Mapped[Weekday] = mapped_column(Enum(Weekday, name='weekday_enums'), nullable=False)
    start_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)
    end_time: Mapped[datetime.time] = mapped_column(Time, nullable=False)

    slot_duration_minutes: Mapped[orm_fields.not_nullable_int]
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)