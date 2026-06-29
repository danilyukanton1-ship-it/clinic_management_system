from sqlalchemy.ext.asyncio import AsyncSession
from app.medical_records.schemas.disease import DiseaseCreateSchema, DiseaseUpdateSchema
from app.medical_records.exceptions.disease import DiseaseNotFoundException, DiseaseAlreadyExistsException
from app.medical_records.models.disease import Disease
from db.unit_of_work import UnitOfWork

class DiseaseService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(session=self.session)

    async def create(self, data: DiseaseCreateSchema) -> Disease:
        disease = await self.uow.diseases.get_disease_by_code(disease_code=data.code)
        if disease:
            raise DiseaseAlreadyExistsException()
        disease = await self.uow.diseases.get_disease_by_name(name=data.name)
        if disease:
            raise DiseaseAlreadyExistsException()
        async with self.uow:
            disease = await self.uow.diseases.create_disease(data=data)
        return disease

    async def update(self, disease_id: int, data: DiseaseUpdateSchema) -> Disease:
        disease = await self.uow.diseases.get_disease_by_id(disease_id)
        if not disease:
            raise DiseaseNotFoundException()
        disease_by_name = await self.uow.diseases.get_disease_by_name(name=data.name)
        if disease_by_name:
            raise DiseaseAlreadyExistsException()
        disease_by_code = await self.uow.diseases.get_disease_by_code(code=data.code)
        if disease_by_code:
            raise DiseaseAlreadyExistsException()
        async with self.uow:
            updated_disease = await self.uow.diseases.update_disease(disease=disease, data=data)
        return updated_disease

    async def get_all(self) -> list[Disease]:
        diseases = await self.uow.diseases.get_all_diseases()
        if not diseases:
            raise DiseaseNotFoundException()
        return diseases

    async def get_by_code(self, disease_code: str) -> Disease:
        disease = await self.uow.diseases.get_disease_by_code(disease_code=disease_code)
        if not disease:
            raise DiseaseNotFoundException()
        return disease

    async def get_by_name(self, name: str) -> Disease:
        disease = await self.uow.diseases.get_disease_by_name(disease_name=name)
        if not disease:
            raise DiseaseNotFoundException()
        return disease

    async def delete(self, disease_id: int) -> None:
        disease = await self.uow.diseases.get_disease_by_id(disease_id=disease_id)
        if not disease:
            raise DiseaseNotFoundException()
        async with self.uow:
            await self.uow.diseases.delete_disease(disease=disease)
        return None


