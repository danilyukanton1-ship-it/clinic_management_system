from sqlalchemy import select

from app.medical_records.models.prescription import Prescription
from app.medical_records.schemas.prescription import (
    PrescriptionCreateSchema,
    PrescriptionUpdateSchema,
)
from core.repository import BaseRepository


class PrescriptionRepository(BaseRepository):
    async def create_prescription(self, data: PrescriptionCreateSchema):
        prescription = Prescription(
            appointment_id=data.appointment_id,
            recommendations=data.recommendations,
        )
        self.session.add(prescription)
        await self.session.flush()
        await self.session.refresh(prescription)
        return prescription

    async def get_prescription_by_appointment_id(
        self, appointment_id: int
    ) -> Prescription | None:
        stmt = select(Prescription).where(Prescription.appointment_id == appointment_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_prescription_by_id(self, prescription_id: int) -> Prescription | None:
        stmt = select(Prescription).where(Prescription.id == prescription_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_prescription(self, prescription: Prescription) -> None:
        await self.session.delete(prescription)
        await self.session.flush()
        await self.session.refresh(prescription)

    async def update_prescription(
        self, prescription: Prescription, data: PrescriptionUpdateSchema
    ) -> Prescription:
        prescription.recommendations = data.recommendations
        await self.session.flush()
        await self.session.refresh(prescription)
        return prescription
