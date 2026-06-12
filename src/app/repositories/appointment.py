from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.appointment import Appointment

class AppointmentRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, appointment: Appointment) -> Appointment:
        self.session.add(appointment)
        await self.session.flush()
        await self.session.refresh(appointment)
        return appointment

    async def get_by_id(self, appointment_id: int) -> Appointment | None:
        stmt = (
            select(Appointment).where(Appointment.id == appointment_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_slot_id(self, slot_id: int) -> Appointment | None:
        stmt = (
            select(Appointment)
            .where(Appointment.slot_id == slot_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_patient_appointments(self, patient_id: int) -> list[Appointment]:
        stmt = (
            select(Appointment)
            .where(Appointment.patient_id == patient_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_doctor_appointments(self, doctor_id: int) -> list[Appointment]:
        stmt = (
            select(Appointment)
            .where(Appointment.doctor_id == doctor_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete(self, appointment: Appointment) -> None:
        await self.session.delete(appointment)

