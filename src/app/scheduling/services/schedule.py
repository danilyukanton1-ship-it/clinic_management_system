from sqlalchemy.ext.asyncio import AsyncSession

from app.scheduling.exceptions.schedule import ScheduleNotFoundException, ScheduleAlreadyExistsException
from app.scheduling.schemas.schedule import ScheduleCreateSchema, ScheduleUpdateSchema, ScheduleResponseSchema
from app.scheduling.services.schedule_slot import ScheduleSlotService
from app.users.exceptions.user import UserNotFoundException

from common.enums.weekday import Weekday
from db.unit_of_work import UnitOfWork


class ScheduleService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.schedule_slot_service = ScheduleSlotService(session=self.session)
        self.uow = UnitOfWork(session=self.session)

    async def get_schedule_by_doctor_id(self, doctor_id: int, weekday: Weekday) -> ScheduleResponseSchema:
        schedule = await self.uow.schedules.get_schedule_by_doctor_id(doctor_id=doctor_id, weekday=weekday)
        if not schedule:
            raise ScheduleNotFoundException()
        return ScheduleResponseSchema.model_validate(schedule)

    async def get_by_id(self, schedule_id: int) -> ScheduleResponseSchema:
        schedule = await self.uow.schedules.get_schedule_by_id(schedule_id=schedule_id)
        if not schedule:
            raise ScheduleNotFoundException()
        return ScheduleResponseSchema.model_validate(schedule)

    async def create_schedule(self, schedule: ScheduleCreateSchema) -> ScheduleResponseSchema:
        async with self.uow:
            if await self.uow.schedules.if_exists(doctor_id=schedule.doctor_id, weekday=schedule.weekday):
                raise ScheduleAlreadyExistsException()
            schedule = await self.uow.schedules.create_schedule(schedule=schedule)
            await self.schedule_slot_service.create_slots_for_schedule(schedule=schedule)
        return ScheduleResponseSchema.model_validate(schedule)

    async def update_schedule(self, doctor_id: int, data: ScheduleUpdateSchema) -> ScheduleResponseSchema:
        async with self.uow:
            doctor = await self.uow.users.get_doctor_by_id(doctor_id=doctor_id)
            if not doctor:
                raise UserNotFoundException()
            db_schedule = await self.uow.schedules.get_schedule_by_doctor_id(doctor_id=doctor_id, weekday=data.weekday.value)
            if not db_schedule:
                raise ScheduleNotFoundException()
            schedule = await self.uow.schedules.update_schedule(db_schedule=db_schedule, data=data)
        return ScheduleResponseSchema.model_validate(schedule)

