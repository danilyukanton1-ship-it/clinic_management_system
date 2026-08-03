from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.scheduling.exceptions.schedule import (
    ScheduleAlreadyExistsException,
    ScheduleCanNotBeDeletedException,
    ScheduleNotFoundException,
)
from app.scheduling.schemas.schedule import (
    ScheduleCreateSchema,
    ScheduleResponseSchema,
    ScheduleUpdateSchema,
)
from app.users.exceptions.user import UserNotFoundException
from common.enums.slot_status import SlotStatus
from common.enums.weekday import Weekday
from db.unit_of_work import UnitOfWork


class ScheduleService:

    def __init__(self, session: AsyncSession):
        self.uow = UnitOfWork(session=session)

    async def get_schedule_by_doctor_id_and_weekday(
        self, doctor_id: int, weekday: Weekday
    ) -> ScheduleResponseSchema:
        schedule = await self.uow.schedules.get_by_doctor_id_and_weekday(
            doctor_id=doctor_id, weekday=weekday
        )
        if not schedule:
            raise ScheduleNotFoundException()
        return ScheduleResponseSchema.model_validate(schedule)

    async def get_schedule_by_doctor_id_and_weekday_for_admin(
        self,
        doctor_id: int,
        weekday: Weekday,
    ) -> list[ScheduleResponseSchema]:
        schedules = await self.uow.schedules.get_by_doctor_id_and_weekday_for_admin(
            doctor_id=doctor_id, weekday=weekday
        )
        if not schedules:
            raise ScheduleNotFoundException()
        return [
            ScheduleResponseSchema.model_validate(schedule) for schedule in schedules
        ]

    async def get_schedule_by_id(
        self, schedule_id: int, admin: bool | None = None
    ) -> ScheduleResponseSchema:
        schedule = await self.uow.schedules.get_by_id(
            schedule_id=schedule_id, admin=admin
        )
        if not schedule:
            raise ScheduleNotFoundException()
        return ScheduleResponseSchema.model_validate(schedule)

    async def get_all_schedule_by_doctor_id(
        self, doctor_id: int, admin: bool | None = None
    ) -> list[ScheduleResponseSchema]:
        schedules = await self.uow.schedules.get_all_by_doctor_id(
            doctor_id=doctor_id, admin=admin
        )
        if not schedules:
            raise ScheduleNotFoundException()
        return [
            ScheduleResponseSchema.model_validate(schedule) for schedule in schedules
        ]

    async def create(self, data: ScheduleCreateSchema) -> ScheduleResponseSchema:
        async with self.uow:
            if not await self.uow.users.get_doctor_by_id(doctor_id=data.doctor_id):
                raise UserNotFoundException()
            if await self.uow.schedules.if_exists(
                doctor_id=data.doctor_id, weekday=data.weekday
            ):
                raise ScheduleAlreadyExistsException()
            schedule = await self.uow.schedules.create_schedule(schedule=data)
        return ScheduleResponseSchema.model_validate(schedule)

    async def update(
        self, doctor_id: int, weekday: Weekday, data: ScheduleUpdateSchema
    ) -> ScheduleResponseSchema:
        async with self.uow:
            db_schedule = await self.uow.schedules.get_by_doctor_id_and_weekday(
                doctor_id=doctor_id, weekday=weekday
            )
            if not db_schedule:
                raise ScheduleNotFoundException()
            last_booked = await self.uow.schedule_slots.get_last_booked_datetime(
                doctor_id=doctor_id, schedule_id=db_schedule.id
            )
            start_delete_date = (
                last_booked.date() + timedelta(days=1) if last_booked else datetime.now(UTC).date()
            )
            slots_to_delete = await self.uow.schedule_slots.get_slots_after_date(
                doctor_id=doctor_id, day=start_delete_date, schedule_id=db_schedule.id
            )
            for slot in slots_to_delete:
                await self.uow.schedule_slots.delete_slot(slot=slot)
            schedule = await self.uow.schedules.update_schedule(
                db_schedule=db_schedule, data=data
            )
        return ScheduleResponseSchema.model_validate(schedule)

    async def deactivate_schedule(self, schedule_id: int) -> None:
        async with self.uow:
            schedule = await self.uow.schedules.get_by_id(schedule_id=schedule_id)
            if not schedule:
                raise ScheduleNotFoundException()
            booked_slots = (
                await self.uow.schedule_slots.get_future_slots_by_doctor_id_status(
                    doctor_id=schedule.doctor_id,
                    status=SlotStatus.BOOKED,
                    weekday=schedule.weekday,
                )
            )
            if not booked_slots:
                slots_to_delete = await self.uow.schedule_slots.get_slots_after_date(
                    doctor_id=schedule.doctor_id,
                    day=datetime.now(UTC).date(),
                    schedule_id=schedule_id,
                )
                for slot in slots_to_delete:
                    await self.uow.schedule_slots.delete_slot(slot=slot)
            else:
                raise ScheduleCanNotBeDeletedException()
            await self.uow.schedules.make_schedule_unactive(schedule=schedule)
