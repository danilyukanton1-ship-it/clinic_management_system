from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.schedule_slot import ScheduleSlotRepository


class ScheduleSlotService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.schedule_slot_repo = ScheduleSlotRepository(session)


    async def get_free_slots(self):
        slots = await self.schedule_slot_repo.get_free_slots()
        return list(slots)
