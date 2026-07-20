from sqlalchemy.ext.asyncio import AsyncSession
from app.users.models.user import User
from app.appoinments.exceptions.appointment import AppointmentNotFoundException
from app.medical_records.exceptions.prescription import PrescriptionNotFoundException
from app.medical_records.schemas.prescription import PrescriptionResponseSchema, PrescriptionUpdateSchema
from db.unit_of_work import UnitOfWork
from app.medical_records.policy.prescription import PrescriptionPolicy


class PrescriptionService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.policy = PrescriptionPolicy()
        self.uow = UnitOfWork(self.session)


    async def update(self, prescription_id: int, data: PrescriptionUpdateSchema, current_user: User) -> PrescriptionResponseSchema:
        async with self.uow:
            prescription = await self.uow.prescriptions.get_prescription_by_id(prescription_id=prescription_id)
            if not prescription:
                raise PrescriptionNotFoundException()
            appointment = await self.uow.appointments.get_appointment_by_prescription_id(
                prescription_id=prescription.id
            )
            if not appointment:
                raise AppointmentNotFoundException()
            self.policy.can_update(user=current_user, appointment=appointment)
            await self.uow.prescriptions.update_prescription(prescription=prescription, data=data)
        return PrescriptionResponseSchema.model_validate(prescription)

