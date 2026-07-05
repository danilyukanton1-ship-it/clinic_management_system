from sqlalchemy.ext.asyncio import AsyncSession

from app.medical_records.schemas.prescription import PrescriptionResponseSchema, PrescriptionUpdateSchema
from db.unit_of_work import UnitOfWork


class PrescriptionService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(self.session)


    async def update(self, prescription_id: int, data: PrescriptionUpdateSchema) -> PrescriptionResponseSchema:
        async with self.uow:
            prescription = await self.uow.prescriptions.get_prescription_by_id(prescription_id=prescription_id)
            await self.uow.prescriptions.update_prescription(prescription=prescription, data=PrescriptionUpdateSchema)
        return PrescriptionResponseSchema(
            id=prescription.id,
            appointment_id=prescription.appointment_id,
            recommendations=prescription.recommendations,
        )

