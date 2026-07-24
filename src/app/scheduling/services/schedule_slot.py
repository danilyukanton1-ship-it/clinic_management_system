from datetime import datetime, timedelta, date, time

from sqlalchemy.ext.asyncio import AsyncSession

from app.scheduling.models.schedule_absence import ScheduleAbsence
from app.scheduling.models.schedule_slot import ScheduleSlot
from app.scheduling.exceptions.schedule import ScheduleNotFoundException
from app.scheduling.models.schedule import Schedule
from app.scheduling.schemas.schedule_slot import ScheduleSlotCreateSchema, ScheduleSlotResponseSchema, \
    ScheduleSlotUpdateSchema
from app.scheduling.exceptions.schedule_slot import (
    SlotNotFoundException,
    SlotStatusCanNotBeChangedException,
    SlotAlreadyBookedException, SlotCanNotBeChangedException
)
from common.constants import WEEKDAY_MAPPING
from common.enums.slot_status import SlotStatus
from db.unit_of_work import UnitOfWork


class ScheduleSlotService:

    def __init__(self, session: AsyncSession):
        self.uow = UnitOfWork(session=session)


    async def _create_slots(
            self,
            slot_start: datetime,
            workday_end: datetime,
            schedule: Schedule,
            absences: ScheduleAbsence | None = None,
        ) -> list[ScheduleSlot]:
        slots = []

        while slot_start < workday_end:
            slot_end = slot_start + timedelta(minutes=schedule.slot_duration_minutes)
            if slot_end > workday_end:
                break
            if (
                slot_start.time() < schedule.lunch_end_time
                and slot_end.time() > schedule.lunch_start_time
            ):
                slot_start = slot_end
                continue
            status = SlotStatus.FREE
            if absences and any(
                    slot_start < absence.end_date
                    and slot_end > absence.start_date
                    for absence in absences
            ):
                status = SlotStatus.BLOCKED
            slot = self.uow.schedule_slots.create_slot_instance(
                schedule_slot=ScheduleSlotCreateSchema(
                    doctor_id=schedule.doctor_id,
                    schedule_id=schedule.id,
                    status=status,
                    slot_start=slot_start,
                    slot_end=slot_end,
                )
            )
            slots.append(slot)
            slot_start = slot_end
        return slots

    async def create_slots(self, start_date: date, end_date: date, doctor_id: int) -> list[ScheduleSlotResponseSchema]:
        async with self.uow:
            doctor_schedules = await self.uow.schedules.get_all_by_doctor_id(doctor_id=doctor_id)
            if not doctor_schedules:
                raise ScheduleNotFoundException()
            slots = []

            current_date = start_date
            while current_date <= end_date:
                schedule = await self.uow.schedules.get_by_doctor_id_and_weekday(
                    doctor_id=doctor_id,
                    weekday=WEEKDAY_MAPPING[current_date.weekday()]
                )
                if not schedule:
                    current_date += timedelta(days=1)
                    continue

                slot_start = datetime.combine(current_date, schedule.start_time)

                workday_end = datetime.combine(current_date, schedule.end_time)
                absences =  await self.uow.absences.get_overlapping_absence(
                        doctor_id=schedule.doctor_id,
                        start_date=datetime.combine(current_date, time.min),
                        end_date=datetime.combine(current_date, time.max),
                    )
                slots.extend(
                    await self._create_slots(
                        slot_start=slot_start,
                        workday_end=workday_end,
                        schedule=schedule,
                        absences=absences,
                    )
                )
                current_date += timedelta(days=1)
            if not slots:
                return []
            await self.uow.schedule_slots.bulk_create_slots(slots)
        return [ScheduleSlotResponseSchema.model_validate(slot) for slot in slots]

    async def change_slot_status(self, slot_id: int, status: SlotStatus) -> ScheduleSlotResponseSchema:
        async with self.uow:
            slot = await self.uow.schedule_slots.get_slot_by_id(slot_id=slot_id)
            if not slot:
                raise SlotNotFoundException()
            if slot.status == SlotStatus.BOOKED and status == SlotStatus.BOOKED:
                raise SlotAlreadyBookedException()
            elif slot.status == status:
                raise SlotStatusCanNotBeChangedException()
            status_changed_slot = await self.uow.schedule_slots.change_slot_status(
                slot=slot,
                status=status,
            )
            return ScheduleSlotResponseSchema.model_validate(status_changed_slot)

    async def get_future_slots_by_doctor_id_status(
            self,
            doctor_id: int,
            status: SlotStatus
    ) -> list[ScheduleSlotResponseSchema]:
        async with self.uow:
            slots = await self.uow.schedule_slots.get_future_slots_by_doctor_id_status(
                doctor_id=doctor_id,
                status=status
            )
            if not slots:
                raise SlotNotFoundException()
            return [ScheduleSlotResponseSchema.model_validate(slot) for slot in slots]

    async def get_past_slots_by_doctor_id_status(
            self,
            doctor_id: int,
            status: SlotStatus
    ) -> list[ScheduleSlotResponseSchema]:
        async with self.uow:
            slots = await self.uow.schedule_slots.get_past_slots_by_doctor_id_status(
                doctor_id=doctor_id,
                status=status
            )
            if not slots:
                raise SlotNotFoundException()
            return [ScheduleSlotResponseSchema.model_validate(slot) for slot in slots]

    async def update(self, slot_id: int, data: ScheduleSlotUpdateSchema) -> ScheduleSlotResponseSchema:
        async with self.uow:
            slot = await self.uow.schedule_slots.get_slot_by_id(slot_id=slot_id)
            if not slot:
                raise SlotNotFoundException()
            if slot.status in (SlotStatus.BOOKED, SlotStatus.BLOCKED):
                raise SlotCanNotBeChangedException()
            overlapping_slots = await self.uow.schedule_slots.get_slots_overlapping_period(
                doctor_id=slot.doctor_id,
                start_date=data.slot_start,
                end_date=data.slot_end,
                exclude_slot_id=slot.id,
            )
            if overlapping_slots:
                raise SlotCanNotBeChangedException()
            slot = await self.uow.schedule_slots.update_slot(slot=slot, data=data)
        return ScheduleSlotResponseSchema.model_validate(slot)


