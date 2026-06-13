from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.schedule_slot import ScheduleSlot
from app.enums.slot_status import SlotStatus

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

    async def get_free_slots(self) -> list[ScheduleSlot]:
        stmt = (
            select(ScheduleSlot)
            .where(status=SlotStatus.FREE)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
