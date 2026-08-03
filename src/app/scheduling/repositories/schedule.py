from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app.scheduling.models.schedule import Schedule
from app.scheduling.schemas.schedule import ScheduleCreateSchema, ScheduleUpdateSchema
from common.enums.weekday import Weekday
from core.config import settings
from core.repository import BaseRepository


class ScheduleRepository(BaseRepository):

    async def create_schedule(self, schedule: ScheduleCreateSchema) -> Schedule:
        schedule = Schedule(
            doctor_id=schedule.doctor_id,
            weekday=schedule.weekday,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            lunch_start_time=schedule.lunch_start_time,
            lunch_end_time=schedule.lunch_end_time,
            slot_duration_minutes=schedule.slot_duration_minutes,
        )
        self.session.add(schedule)
        await self.session.flush()
        await self.session.refresh(schedule)
        return schedule

    async def get_by_id(
        self, schedule_id: int, admin: bool | None = None
    ) -> Schedule | None:
        stmt = select(Schedule).where(
            Schedule.id == schedule_id,
        )
        if not admin:
            stmt = stmt.where(Schedule.is_active.is_(True))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_doctor_id_and_weekday(
        self, doctor_id: int, weekday: Weekday
    ) -> Schedule | None:
        stmt = select(Schedule).where(
            Schedule.doctor_id == doctor_id,
            Schedule.weekday == weekday,
            Schedule.is_active.is_(True),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_doctor_id_and_weekday_for_admin(
        self, doctor_id: int, weekday: Weekday
    ) -> list[Schedule]:
        stmt = select(Schedule).where(
            Schedule.doctor_id == doctor_id,
            Schedule.weekday == weekday,
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_inactive_expired_schedules(self) -> list[Schedule]:
        threshold = datetime.now(UTC) - timedelta(days=settings.SLOT_RETENTION_DAYS)
        stmt = select(Schedule).where(
            Schedule.is_active.is_(False),
            Schedule.updated_at < threshold,
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_all_by_doctor_id(
        self, doctor_id: int, admin: bool | None = None
    ) -> list[Schedule] | None:
        stmt = select(Schedule).where(
            Schedule.doctor_id == doctor_id,
        )
        if not admin:
            stmt = stmt.where(Schedule.is_active.is_(True))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_schedule(
        self, db_schedule: Schedule, data: ScheduleUpdateSchema
    ) -> Schedule:
        db_schedule.start_time = data.start_time
        db_schedule.end_time = data.end_time
        db_schedule.lunch_start_time = data.lunch_start_time
        db_schedule.lunch_end_time = data.lunch_end_time
        db_schedule.slot_duration_minutes = data.slot_duration_minutes
        await self.session.flush()
        await self.session.refresh(db_schedule)
        return db_schedule

    async def if_exists(self, doctor_id: int, weekday: Weekday) -> bool:
        stmt = select(Schedule).where(
            Schedule.doctor_id == doctor_id,
            Schedule.weekday == weekday,
            Schedule.is_active.is_(True),
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def delete_schedule(self, schedule: Schedule) -> None:
        await self.session.delete(schedule)

    async def make_schedule_unactive(self, schedule: Schedule) -> Schedule:
        schedule.is_active = False
        await self.session.flush()
        await self.session.refresh(schedule)
