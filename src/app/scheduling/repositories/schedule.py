from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.scheduling.models.schedule import Schedule
from app.scheduling.schemas.schedule import ScheduleCreateSchema, ScheduleUpdateSchema
from common.enums.weekday import Weekday

class ScheduleRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_schedule(self, schedule: ScheduleCreateSchema) -> Schedule:
        schedule = Schedule(
            doctor_id=schedule.doctor_id,
            weekday=schedule.weekday,
            start_time=schedule.start_time,
            end_time=schedule.end_time,
            slot_duration_minutes=schedule.slot_duration_minutes,
        )
        self.session.add(schedule)
        await self.session.flush()
        await self.session.refresh(schedule)
        return schedule

    async def get_schedule_by_id(self, schedule_id: int) -> Schedule | None:
        stmt = (
            select(Schedule)
            .where(Schedule.id == schedule_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_schedule_by_doctor_id(self, doctor_id: int, weekday: Weekday) -> Schedule | None:
        stmt = (
            select(Schedule)
            .where(Schedule.doctor_id == doctor_id, Schedule.weekday == weekday)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_schedule(self, db_schedule: Schedule, data: ScheduleUpdateSchema) -> Schedule:
        db_schedule.start_time = data.start_time
        db_schedule.end_time = data.end_time
        db_schedule.slot_duration_minutes = data.slot_duration_minutes
        await self.session.flush()
        await self.session.refresh(db_schedule)
        return db_schedule

    async def if_exists(self, doctor_id: int, weekday: Weekday) -> bool:
        stmt = (
            select(Schedule).where(Schedule.doctor_id == doctor_id, Schedule.weekday == weekday)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

