from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.appointment import AppointmentRepository
from app.repositories.schedule_slot import ScheduleSlotRepository
from app.schemas.appointment import AppointmentCreateSchema

from app.exceptions.schedule_slot import SlotNotFoundException, SlotNotAvailableException

from app.enums.slot_status import SlotStatus

class AppointmentService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.appointment_repo = AppointmentRepository(session)
        self.schedule_slot_repo = ScheduleSlotRepository(session)

    async def create_appointment(self, appointment: AppointmentCreateSchema):
        slot = await self.schedule_slot_repo.get_slot_by_id(appointment.slot_id)
        if slot is None:
            raise SlotNotFoundException()
        if slot.status != SlotStatus.FREE:
            raise SlotNotAvailableException()

        appointment = await self.appointment_repo.create(appointment)
        return appointment

    async def get_all_appointments(self):
        appointments = await self.appointment_repo.get_all_appointments()
        return appointments
