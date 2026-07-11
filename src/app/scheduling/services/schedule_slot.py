from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from app.scheduling.models.schedule import Schedule
from app.scheduling.schemas.schedule_slot import ScheduleSlotCreateSchema
from app.scheduling.exceptions.schedule_slot import SlotAlreadyBookedException
from common.constants import WEEKDAY_MAPPING
from db.unit_of_work import UnitOfWork


class ScheduleSlotService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(session=self.session)


    async def get_free_slots(self):
        slots = await self.uow.schedule_slots.get_free_slots()
        return list(slots)

    async def create_slots_for_schedule(self, schedule: Schedule):
        slots = []

        today = datetime.now().date()
        end_date = today + timedelta(days=30)

        current_date = today
        while current_date <= end_date:

            if current_date.weekday() == WEEKDAY_MAPPING[schedule.weekday]:
                slot_start = datetime.combine(current_date, schedule.start_time)

                workday_end = datetime.combine(current_date, schedule.end_time)

                while slot_start < workday_end:
                    slot_end = slot_start + timedelta(minutes=schedule.slot_duration_minutes)

                    slot = self.uow.schedule_slots.create_slot_instance(
                        schedule_slot=ScheduleSlotCreateSchema(
                            doctor_id=schedule.doctor_id,
                            schedule_id=schedule.id,
                            slot_start=slot_start,
                            slot_end=slot_end,
                        )
                    )
                    slots.append(slot)

                    slot_start = slot_end

            current_date += timedelta(days=1)
        print(f"slots count = {len(slots)}")
        if not slots:
            return []
        await self.uow.schedule_slots.bulk_create_slots(slots)
        return slots


    async def maked_the_slot_booked(self, slot_id: int):
        async with self.uow:
            slot = await self.uow.schedule_slots.get_slot_for_booking(slot_id)
            if not slot:
                raise SlotAlreadyBookedException()
            booked_slot = await self.uow.schedule_slots.book_slot(slot=slot)
            return booked_slot