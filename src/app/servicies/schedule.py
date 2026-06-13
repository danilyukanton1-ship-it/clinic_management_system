from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schedule import Schedule
from app.repositories.schedule import ScheduleRepository
from app.schemas.schedule import ScheduleCreateSchema, ScheduleUpdateSchema

from app.enums.weekday import Weekday

class ScheduleService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.schedule_repo = ScheduleRepository(session)

    async def if_exists(self, doctor_id: int) -> bool:
        return await self.schedule_repo.if_exists(doctor_id=doctor_id)

    async def get_schedule_by_doctor_id(self, doctor_id: int) -> list[Schedule]:

        schedule = await self.schedule_repo.get_schedule_by_doctor_id(doctor_id=doctor_id)
        return schedule

    async def create_schedule(self, schedule: ScheduleCreateSchema) -> Schedule:
        schedule = await self.schedule_repo.create_schedule(schedule=schedule)
        return schedule

    async def update_schedule(self, schedule: ScheduleUpdateSchema) -> Schedule:
        schedule = await self.schedule_repo.update_schedule_by_doctor_id(schedule=schedule)
        return schedule