from datetime import datetime

from sqlalchemy import select, or_
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.appointments.models.appointment import Appointment
from app.appointments.schemas.appointment import AppointmentCreateSchema
from app.scheduling.models.schedule_slot import ScheduleSlot
from app.medical_records.models.diagnosis import Diagnosis
from app.medical_records.models.prescription import Prescription
from app.medical_records.models.prescription_item import PrescriptionItem
from app.users.models.user import User

class AppointmentRepository:

    def __init__(self, session: AsyncSession ):
        self.session = session

    async def create(self, data: AppointmentCreateSchema) -> Appointment:
        appointment = Appointment(
            patient_id=data.patient_id,
            doctor_id=data.doctor_id,
            slot_id=data.slot_id,
            complaint=data.complaint,
        )
        self.session.add(appointment)
        await self.session.flush()
        return appointment

    async def get_appointment_by_id_with_relations(self, appointment_id: int) -> Appointment | None:
        stmt = (
            select(Appointment)
            .where(
                Appointment.id == appointment_id,
            )
            .options(
                joinedload(Appointment.patient),
                joinedload(Appointment.slot),
                joinedload(Appointment.doctor).joinedload(User.specialization),
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_appointment_by_id(self, appointment_id: int) -> Appointment | None:
        stmt = (
            select(Appointment)
            .where(Appointment.id == appointment_id)
            )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_upcoming_appointments_for_reminder(self, start: datetime, end: datetime) -> list[Appointment]:
        stmt = (
            select(Appointment)
            .join(Appointment.slot)
            .where(
                ScheduleSlot.slot_start >= start,
                ScheduleSlot.slot_start < end,
            )
            .options(
                joinedload(Appointment.patient),
                joinedload(Appointment.slot),
                joinedload(Appointment.doctor).joinedload(User.specialization),
            )
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

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

    async def get_appointment_by_diagnosis_id(
            self,
            diagnosis_id: int,
    ) -> Appointment | None:
        stmt = (
            select(Appointment)
            .join(
                Prescription,
                Prescription.appointment_id == Appointment.id,
            )
            .join(
                Diagnosis,
                Diagnosis.prescription_id == Prescription.id,
            )
            .where(Diagnosis.id == diagnosis_id)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_appointment_by_prescription_id(
        self,
        prescription_id: int,
    ) -> Appointment | None:
        stmt = (
            select(Appointment)
            .join(
                Prescription,
                Prescription.appointment_id == Appointment.id,
            )
            .where(Prescription.id == prescription_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_appointment_by_prescription_item_id(
        self,
        prescription_item_id: int,
    ) -> Appointment | None:
        stmt = (
            select(Appointment)
            .join(
                Prescription,
                Prescription.appointment_id == Appointment.id,
            )
            .join(
                PrescriptionItem,
                PrescriptionItem.prescription_id == Prescription.id,
            )
            .where(PrescriptionItem.id == prescription_item_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def delete_appointment(self, appointment: Appointment) -> None:
        await self.session.delete(appointment)
        await self.session.flush()
        return None

