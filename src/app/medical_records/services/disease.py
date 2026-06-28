from sqlalchemy.ext.asyncio import AsyncSession
from app.medical_records.schemas.disease import DiseaseCreateSchema, DiseaseUpdateSchema
from app.medical_records.exceptions.disease import DiseaseNotFoundException
from app.medical_records.models.disease import Disease
from db.unit_of_work import UnitOfWork

class DiseaseService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(session=self.session)

    async def create(self, data: DiseaseCreateSchema) -> Disease:
        async with self.uow:
            disease = await self.uow.disease.create_disease(data=data)
        return disease

    async def update(self, disease_id: int, data: DiseaseUpdateSchema) -> Disease:
        disease = await self.uow.disease.get_disease_by_id(disease_id)
        if not disease:
            raise DiseaseNotFoundException()
        async with self.uow:
            updated_disease = await self.uow.disease.update_disease(disease=disease, data=data)
        return updated_disease

    async def get_all(self) -> list[Disease]:
        return await self.uow.disease.get_all_diseases()

    async def get_by_code(self, disease_code: str) -> Disease:
        disease = await self.uow.disease.get_disease_by_code(disease_code=disease_code)
        return disease

    async def get_by_name(self, name: str) -> Disease:
        disease = await self.uow.disease.get_disease_by_name(disease_name=name)
        return disease

    async def delete(self, disease_id: int) -> None:
        disease = await self.uow.disease.get_disease_by_id(disease_id=disease_id)
        if not disease:
            raise DiseaseNotFoundException()
        async with self.uow:
            await self.uow.disease.delete_disease(disease=disease)
        return None


