from sqlalchemy.ext.asyncio import AsyncSession

from app.scheduling.repositories.schedule_slot import ScheduleSlotRepository
from app.appoinments.repositories.appointment import AppointmentRepository
from app.scheduling.repositories.schedule import ScheduleRepository
from app.users.repositories.user import UserRepository
from app.users.repositories.specialization import SpecializationRepository

class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

        self.schedule_slots = ScheduleSlotRepository(session)
        self.appointments = AppointmentRepository(session)
        self.schedules = ScheduleRepository(session)
        self.users = UserRepository(session)
        self.specializations = SpecializationRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

