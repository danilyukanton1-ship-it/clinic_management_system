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
        await self.session.flush()
        return appointment

