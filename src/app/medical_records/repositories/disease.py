from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.medical_records.schemas.disease import DiseaseCreateSchema, DiseaseUpdateSchema
from app.medical_records.models.disease import Disease

class DiseaseRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_disease(self, data: DiseaseCreateSchema) -> Disease:
        disease = Disease(
            code=data.code,
            name=data.name,
            description=data.description,
        )
        self.session.add(disease)
        await self.session.flush()
        await self.session.refresh(disease)
        return disease

    async def get_disease_by_id(self, disease_id: int) -> Disease | None:
        stmt = (
            select(Disease)
            .where(Disease.id==disease_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_disease_by_code(self, disease_code: str) -> Disease | None:
        stmt = (
            select(Disease)
            .where(Disease.code==disease_code)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_disease_by_name(self, disease_name: str) -> Disease | None:
        stmt = (
            select(Disease)
            .where(Disease.name==disease_name)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all_diseases(self) -> list[Disease]:
        stmt = (
            select(Disease)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_disease(self, disease: Disease, data: DiseaseUpdateSchema) -> Disease:
        disease.code = data.code
        disease.name = data.name
        disease.description = data.description
        await self.session.flush()
        await self.session.refresh(disease)
        return disease

    async def delete_disease(self, disease: Disease) -> None:
        return await self.session.delete(disease)



