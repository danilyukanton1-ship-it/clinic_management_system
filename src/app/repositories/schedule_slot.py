from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.schedule_slot import ScheduleSlot

class ScheduleSlotRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_slot_by_id(self, slot_id: int) -> ScheduleSlot:
        stmt = (
            select(ScheduleSlot)
            .where(ScheduleSlot.id == slot_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

