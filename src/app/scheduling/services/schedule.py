from sqlalchemy.ext.asyncio import AsyncSession

from app.scheduling.models.schedule import Schedule
from app.scheduling.repositories.schedule import ScheduleRepository
from app.scheduling.schemas.schedule import ScheduleCreateSchema, ScheduleUpdateSchema
from app.scheduling.services.schedule_slot import ScheduleSlotService

from common.enums.weekday import Weekday

class ScheduleService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.schedule_repo = ScheduleRepository(session)
        self.schedule_slots_service = ScheduleSlotService(session)

    async def if_exists(self, weekday: Weekday, doctor_id: int) -> bool:
        return await self.schedule_repo.if_exists(doctor_id=doctor_id, weekday=weekday)

    async def get_schedule_by_doctor_id(self, doctor_id: int) -> list[Schedule]:

        schedule = await self.schedule_repo.get_schedule_by_doctor_id(doctor_id=doctor_id)
        return schedule

    async def create_schedule(self, schedule: ScheduleCreateSchema) -> Schedule:
        schedule = await self.schedule_repo.create_schedule(schedule=schedule)
        await self.schedule_slots_service.create_slots_for_schedule(schedule=schedule)
        return schedule

    async def update_schedule(self, schedule: ScheduleUpdateSchema) -> Schedule:
        schedule = await self.schedule_repo.update_schedule_by_doctor_id(schedule=schedule)
        return schedule