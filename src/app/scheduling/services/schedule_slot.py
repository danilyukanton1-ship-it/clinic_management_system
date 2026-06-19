from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from app.scheduling.models.schedule import Schedule
from app.scheduling.repositories.schedule_slot import ScheduleSlotRepository
from app.scheduling.schemas.schedule_slot import ScheduleSlotCreateSchema
from app.scheduling.exceptions.schedule_slot import SlotNotFoundException
from common.constants import WEEKDAY_MAPPING

class ScheduleSlotService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.schedule_slot_repo = ScheduleSlotRepository(session)


    async def get_free_slots(self):
        slots = await self.schedule_slot_repo.get_free_slots()
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

                    slot = self.schedule_slot_repo.build_slot(
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
        await self.schedule_slot_repo.bulk_create_slots(slots)
        return slots


    async def maked_the_slot_booked(self, slot_id: int):
        slot = await self.schedule_slot_repo.get_slot_by_id(slot_id)
        if not slot:
            raise SlotNotFoundException()
        pass

