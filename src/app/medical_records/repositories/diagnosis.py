from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.medical_records.schemas.diagnosis import DiagnosisCreateSchema, DiagnosisUpdateSchema
from app.medical_records.models.diagnosis import Diagnosis

class DiagnosisRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_diagnosis(self, data: DiagnosisCreateSchema) -> Diagnosis:
        diagnosis = Diagnosis(
            prescription_id=data.prescription_id,
            disease_id=data.disease_id,
            notes=data.notes,
        )
        self.session.add(diagnosis)
        await self.session.flush()
        await self.session.refresh(diagnosis)
        return diagnosis

    async def update_diagnosis(self,diagnosis: Diagnosis, data: DiagnosisUpdateSchema) -> Diagnosis:
        diagnosis.prescription_id = data.prescription_id
        diagnosis.disease_id = data.disease_id
        diagnosis.notes = data.notes
        await self.session.flush()
        await self.session.refresh(diagnosis)
        return diagnosis

    async def get_all_diagnoses(self) -> list[Diagnosis]:
        stmt = (
            select(Diagnosis)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_diagnosis_by_id(self, diagnosis_id: int) -> Diagnosis | None:
        stmt = (
            select(Diagnosis)
            .where(Diagnosis.id == diagnosis_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().one()

    async def get_diagnoses_by_prescription_id(self, prescription_id: int) -> list[Diagnosis]:
        stmt = (
            select(Diagnosis)
            .where(Diagnosis.prescription_id == prescription_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_diagnoses_by_disease_id(self, disease_id: int) -> list[Diagnosis]:
        stmt = (
            select(Diagnosis)
            .where(Diagnosis.disease_id==disease_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def delete_diagnosis(self, diagnosis: Diagnosis) -> None:
        await self.session.delete(diagnosis)
        return None