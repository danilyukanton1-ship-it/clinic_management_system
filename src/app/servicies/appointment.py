from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.appointment import AppointmentRepository
from app.repositories.schedule_slot import ScheduleSlotRepository


class AppointmentService:

    def __init__(
            self,
            session: AsyncSession,
        ):
        self.appointment_repo = AppointmentRepository(session)
        self.schedule_slot_repo = ScheduleSlotRepository(session)

