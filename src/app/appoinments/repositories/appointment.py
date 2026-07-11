from datetime import datetime

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.appoinments.models.appointment import Appointment
from app.appoinments.schemas.appointment import AppointmentCreateSchema
from app.scheduling.models.schedule_slot import ScheduleSlot

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

    async def get_appointments(self) -> list[Appointment]:
        stmt = (
            select(Appointment).order_by(Appointment.created_at)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_appointment_by_id(self, appointment_id: int) -> Appointment:
        stmt = (
            select(Appointment)
            .where(Appointment.id == appointment_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_future_appointments_by_user_id(self, user_id: int) -> list[Appointment]:
        stmt = (
            select(Appointment)
            .join(Appointment.slot)
            .where(
                or_(
                    Appointment.patient_id == user_id,
                    Appointment.doctor_id == user_id,
                ),
                ScheduleSlot.slot_start >= datetime.now()
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_past_appointments_by_user_id(self, user_id: int) -> list[Appointment]:
        stmt = (
            select(Appointment)
            .join(Appointment.slot)
            .where(
                or_(
                    Appointment.patient_id == user_id,
                    Appointment.doctor_id == user_id,
                ),
                ScheduleSlot.slot_start <= datetime.now()
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())