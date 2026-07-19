from sqlalchemy.ext.asyncio import AsyncSession

from app.appoinments.schemas.appointment import AppointmentCreateSchema, AppointmentResponseSchema

from app.scheduling.exceptions.schedule_slot import SlotNotFoundException, SlotNotAvailableException
from app.users.exceptions.user import UserNotFoundException

from common.enums.slot_status import SlotStatus
from db.unit_of_work import UnitOfWork


class AppointmentService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(session=self.session)

    async def create_appointment(self, appointment: AppointmentCreateSchema):
        async with self.uow:
            slot = await self.uow.schedule_slots.get_slot_by_id(appointment.slot_id)
            if slot is None:
                raise SlotNotFoundException()
            if slot.status != SlotStatus.FREE:
                raise SlotNotAvailableException()

            await self.uow.schedule_slots.change_slot_status(slot=slot, status=SlotStatus.BOOKED)
            appointment = await self.uow.appointments.create(appointment)
            return appointment

    async def get_all_appointments(self):
        appointments = await self.uow.appointments.get_appointments()
        return appointments

    async def get_future_apps_by_user_id(self, user_id: int) -> list[AppointmentResponseSchema]:
        async with self.uow:
            user = await self.uow.users.get_user_by_id(user_id)
            if user is None:
                raise UserNotFoundException()
            appointments = await self.uow.appointments.get_future_appointments_by_user_id(user_id=user_id)
            return [AppointmentResponseSchema.model_validate(appointment) for appointment in appointments]

    async def get_past_apps_by_user_id(self, user_id: int) -> list[AppointmentResponseSchema]:
        async with self.uow:
            user = await self.uow.users.get_user_by_id(user_id)
            if user is None:
                raise UserNotFoundException()
            appointments = await self.uow.appointments.get_past_appointments_by_user_id(user_id=user_id)
            return [AppointmentResponseSchema.model_validate(appointment) for appointment in appointments]