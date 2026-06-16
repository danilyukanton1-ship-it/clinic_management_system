from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.appointment import Appointment
from app.schemas.appointment import AppointmentCreateSchema

class AppointmentRepository:

    def __init__(self, session: AsyncSession ):
        self.session = session

    async def create(self, appointment: AppointmentCreateSchema) -> Appointment:
        appointment = Appointment(
            patient_id=appointment.patient,
            doctor_id=appointment.doctor,
            slot_id=appointment.slot_id,
            complaint=appointment.complaint,
        )
        self.session.add(appointment)
        await self.session.commit()
        await self.session.refresh(appointment)
        return appointment

    async def get_all_appointments(self) -> list[Appointment]:
        stmt = (
            select(Appointment).order_by(Appointment.created_at)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
