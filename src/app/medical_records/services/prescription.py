from sqlalchemy.ext.asyncio import AsyncSession

from app.appointments.exceptions.appointment import AppointmentNotFoundException
from app.medical_records.exceptions.prescription import PrescriptionNotFoundException
from app.medical_records.policy.prescription import PrescriptionPolicy
from app.medical_records.schemas.prescription import (
    PrescriptionResponseSchema,
    PrescriptionUpdateSchema,
)
from app.users.models.user import User
from db.unit_of_work import UnitOfWork


class PrescriptionService:

    def __init__(self, session: AsyncSession):
        self.policy = PrescriptionPolicy()
        self.uow = UnitOfWork(session)

    async def update(
        self, prescription_id: int, data: PrescriptionUpdateSchema, current_user: User
    ) -> PrescriptionResponseSchema:
        async with self.uow:
            prescription = await self.uow.prescriptions.get_prescription_by_id(
                prescription_id=prescription_id
            )
            if not prescription:
                raise PrescriptionNotFoundException()
            appointment = (
                await self.uow.appointments.get_appointment_by_prescription_id(
                    prescription_id=prescription.id
                )
            )
            if not appointment:
                raise AppointmentNotFoundException()
            self.policy.can_update(user=current_user, appointment=appointment)
            prescription = await self.uow.prescriptions.update_prescription(
                prescription=prescription, data=data
            )
        return PrescriptionResponseSchema.model_validate(prescription)
