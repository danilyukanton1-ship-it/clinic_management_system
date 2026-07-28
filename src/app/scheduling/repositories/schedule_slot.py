from datetime import datetime, date

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract, exists

from app.appointments.models.appointment import Appointment
from app.scheduling.models.schedule_slot import ScheduleSlot
from app.scheduling.schemas.schedule_slot import ScheduleSlotCreateSchema, ScheduleSlotUpdateSchema
from common.constants import WEEKDAY_MAPPING_REVERSE
from common.enums.slot_status import SlotStatus
from common.enums.weekday import Weekday


class ScheduleSlotRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_slot_by_id(self, slot_id: int) -> ScheduleSlot | None:
        stmt = (
            select(ScheduleSlot)
            .where(ScheduleSlot.id == slot_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def slot_exists(
            self,
            start_time: datetime,
            end_time: datetime,
            doctor_id: int,
    ) -> bool:
        stmt = select(
            exists().where(
                ScheduleSlot.doctor_id == doctor_id,
                ScheduleSlot.slot_start == start_time,
                ScheduleSlot.slot_end == end_time,
            )
        )
        result = await self.session.scalar(stmt)
        return bool(result)

    async def get_slot_for_booking(self, slot_id: int) -> ScheduleSlot | None:
        stmt = (
            select(ScheduleSlot)
            .where(ScheduleSlot.id == slot_id, ScheduleSlot.status == SlotStatus.FREE)
            .with_for_update()
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_last_booked_datetime(self, schedule_id: int, doctor_id: int) -> datetime | None:
        stmt = (
            select(func.max(ScheduleSlot.slot_start))
            .where(
                ScheduleSlot.doctor_id == doctor_id,
                ScheduleSlot.schedule_id == schedule_id,
                ScheduleSlot.status == SlotStatus.BOOKED,
                ScheduleSlot.slot_start >= datetime.now()
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_slots_after_date(
            self,
            schedule_id: int,
            doctor_id: int,
            day: date,
            status: SlotStatus | None = None,
    ) -> list[ScheduleSlot]:
        stmt = (
            select(ScheduleSlot)
            .where(
                ScheduleSlot.doctor_id == doctor_id,
                ScheduleSlot.schedule_id == schedule_id,
                func.date(ScheduleSlot.slot_start) >= day,
                ScheduleSlot.status != SlotStatus.BOOKED,
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_slots_overlapping_period(
            self,
            doctor_id: int,
            start_date: datetime,
            end_date: datetime,
            exclude_slot_id: int | None = None,
    ) -> list[ScheduleSlot]:
        stmt = (
            select(ScheduleSlot)
            .where(
                ScheduleSlot.doctor_id == doctor_id,
                ScheduleSlot.slot_start < end_date,
                ScheduleSlot.slot_end > start_date,
            )
        )
        if exclude_slot_id:
            stmt = stmt.where(ScheduleSlot.id != exclude_slot_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_future_blocked_slots_in_period(
            self,
            doctor_id: int,
            start_date: datetime,
            end_date: datetime,
    ) -> list[ScheduleSlot]:
        stmt = (
            select(ScheduleSlot)
            .where(
                ScheduleSlot.doctor_id == doctor_id,
                ScheduleSlot.status == SlotStatus.BLOCKED,
                ScheduleSlot.slot_start >= datetime.now(),
                ScheduleSlot.slot_start < end_date,
                ScheduleSlot.slot_end > start_date,
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_future_slots_by_doctor_id_status(
            self,
            doctor_id: int,
            status: SlotStatus,
            weekday: Weekday | None = None,
    ) -> list[ScheduleSlot]:
        stmt = (
            select(ScheduleSlot)
            .where(
                ScheduleSlot.doctor_id == doctor_id,
                ScheduleSlot.status == status,
                ScheduleSlot.slot_start >= datetime.now(),
            )
        )
        if weekday:
            stmt = stmt.where(
                extract("dow", ScheduleSlot.slot_start) == WEEKDAY_MAPPING_REVERSE[weekday]
            )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_past_slots_by_doctor_id_status(self, doctor_id: int, status: SlotStatus) -> list[ScheduleSlot]:
        stmt = (
            select(ScheduleSlot)
            .where(
                ScheduleSlot.doctor_id == doctor_id,
                ScheduleSlot.status == status,
                ScheduleSlot.slot_start <= datetime.now(),
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_slots_by_schedule_ids(self,schedule_ids: list[int]) -> list[ScheduleSlot]:
        stmt = (
            select(ScheduleSlot)
            .where(
                ScheduleSlot.schedule_id.in_(schedule_ids),
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete_slot(self, slot: ScheduleSlot) -> None:
        await self.session.delete(slot)
        return None

    async def create_slot(self, schedule_slot: ScheduleSlotCreateSchema) -> ScheduleSlot:
        slot = ScheduleSlot(
            doctor_id=schedule_slot.doctor_id,
            schedule_id=schedule_slot.schedule_id,
            slot_start=schedule_slot.slot_start,
            slot_end=schedule_slot.slot_end,
        )
        self.session.add(slot)
        await self.session.flush()
        await self.session.refresh(slot)
        return slot

    @staticmethod
    def create_slot_instance(schedule_slot: ScheduleSlotCreateSchema) -> ScheduleSlot:
        slot = ScheduleSlot(
            doctor_id=schedule_slot.doctor_id,
            schedule_id=schedule_slot.schedule_id,
            slot_start=schedule_slot.slot_start,
            slot_end=schedule_slot.slot_end,
            status=schedule_slot.status,
        )
        return slot

    async def bulk_create_slots(self, slots: list[ScheduleSlot]) -> list[ScheduleSlot]:
        self.session.add_all(slots)
        await self.session.flush()
        return slots

    async def change_slot_status(self, slot: ScheduleSlot, status: SlotStatus) -> ScheduleSlot:
        slot.status = status
        slot.updated_at = datetime.now()
        await self.session.flush()
        await self.session.refresh(slot)
        return slot

    async def update_slot(self, slot: ScheduleSlot, data: ScheduleSlotUpdateSchema) -> ScheduleSlot:
        slot.slot_start = data.slot_start
        slot.slot_end = data.slot_end
        slot.status = data.status
        slot.updated_at = datetime.now()
        await self.session.flush()
        await self.session.refresh(slot)
        return slot