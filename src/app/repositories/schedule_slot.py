from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.schedule_slot import ScheduleSlot

class ScheduleSlotRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_slot_by_id(self, slot_id: int) -> ScheduleSlot:
        stmt = (
            select(ScheduleSlot)
            .where(ScheduleSlot.id == slot_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_doctor_slots(self, doctor_id: int) -> list[ScheduleSlot]:
        stmt = (
            select(ScheduleSlot)
            .where(ScheduleSlot.doctor_id == doctor_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def is_slot_available(self, slot_id: int) -> bool:
        slot = await self.get_slot_by_id(slot_id)
        if slot is None:
            return False
        return slot.status == 'free'