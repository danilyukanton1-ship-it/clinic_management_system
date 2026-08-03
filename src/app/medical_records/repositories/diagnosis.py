from sqlalchemy import select

from app.medical_records.models.diagnosis import Diagnosis
from app.medical_records.schemas.diagnosis import (
    DiagnosisCreateSchema,
    DiagnosisUpdateSchema,
)
from common.pagination.schemas import PaginationParams, PaginationResult
from core.repository import BaseRepository


class DiagnosisRepository(BaseRepository):

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

    async def update_diagnosis(
        self, diagnosis: Diagnosis, data: DiagnosisUpdateSchema
    ) -> Diagnosis:
        diagnosis.disease_id = data.disease_id
        diagnosis.notes = data.notes
        await self.session.flush()
        await self.session.refresh(diagnosis)
        return diagnosis

    async def get_all_diagnoses(
        self, pagination: PaginationParams
    ) -> PaginationResult[Diagnosis]:
        stmt = select(Diagnosis)
        return await self.paginate(
            stmt=stmt,
            pagination=pagination,
        )

    async def get_diagnosis_by_id(self, diagnosis_id: int) -> Diagnosis | None:
        stmt = select(Diagnosis).where(Diagnosis.id == diagnosis_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_diagnoses_by_prescription_id_with_pagination(
        self, prescription_id: int, pagination: PaginationParams
    ) -> PaginationResult[Diagnosis]:
        stmt = select(Diagnosis).where(Diagnosis.prescription_id == prescription_id)
        return await self.paginate(
            stmt=stmt,
            pagination=pagination,
        )

    async def get_diagnoses_by_prescription_id(
        self, prescription_id: int
    ) -> list[Diagnosis]:
        stmt = select(Diagnosis).where(Diagnosis.prescription_id == prescription_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_diagnoses_by_disease_id(
        self, disease_id: int, pagination: PaginationParams
    ) -> PaginationResult[Diagnosis]:
        stmt = select(Diagnosis).where(Diagnosis.disease_id == disease_id)
        return await self.paginate(
            stmt=stmt,
            pagination=pagination,
        )

    async def delete_diagnosis(self, diagnosis: Diagnosis) -> None:
        await self.session.delete(diagnosis)
