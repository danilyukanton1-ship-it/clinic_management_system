from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.scheduling.models.schedule_slot import ScheduleSlot
from app.scheduling.schemas.schedule_slot import ScheduleSlotCreateSchema
from common.enums.slot_status import SlotStatus

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
            .where(ScheduleSlot.status == SlotStatus.FREE
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_slot(self, schedule_slot: ScheduleSlotCreateSchema) -> ScheduleSlot:
        slot = ScheduleSlot(
            doctor_id=schedule_slot.doctor_id,
            schedule_id=schedule_slot.schedule_id,
            slot_start=schedule_slot.slot_start,
            slot_end=schedule_slot.slot_end,
        )
        self.session.add(slot)
        await self.session.commit()
        await self.session.refresh(slot)
        return slot

    @staticmethod
    def build_slot(schedule_slot: ScheduleSlotCreateSchema) -> ScheduleSlot:
        slot = ScheduleSlot(
            doctor_id=schedule_slot.doctor_id,
            schedule_id=schedule_slot.schedule_id,
            slot_start=schedule_slot.slot_start,
            slot_end=schedule_slot.slot_end,
        )
        return slot

    async def bulk_create_slots(self, slots: list[ScheduleSlot]) -> list[ScheduleSlot]:
        self.session.add_all(slots)
        await self.session.flush()
        await self.session.commit()
        return slots

    async def book_slot(self, slot: ScheduleSlot) -> ScheduleSlot:
        slot.status = SlotStatus.BOOKED
        await self.session.flush()
        return slot
