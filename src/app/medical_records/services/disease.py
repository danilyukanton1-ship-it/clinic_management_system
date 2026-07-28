from sqlalchemy.ext.asyncio import AsyncSession
from app.medical_records.schemas.disease import DiseaseCreateSchema, DiseaseUpdateSchema, DiseaseResponseSchema
from app.medical_records.exceptions.disease import DiseaseNotFoundException, DiseaseAlreadyExistsException
from db.unit_of_work import UnitOfWork

class DiseaseService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(session=self.session)

    async def create(self, data: DiseaseCreateSchema) -> DiseaseResponseSchema:
        disease = await self.uow.diseases.get_disease_by_code(disease_code=data.code)
        if disease:
            raise DiseaseAlreadyExistsException()
        disease = await self.uow.diseases.get_disease_by_name(disease_name=data.name)
        if disease:
            raise DiseaseAlreadyExistsException()
        async with self.uow:
            disease = await self.uow.diseases.create_disease(data=data)
        return DiseaseResponseSchema.model_validate(disease)

    async def update(self, disease_id: int, data: DiseaseUpdateSchema) -> DiseaseResponseSchema:
        disease = await self.uow.diseases.get_disease_by_id(disease_id)
        if not disease:
            raise DiseaseNotFoundException()
        disease_by_name = await self.uow.diseases.get_disease_by_name(disease_name=data.name)
        if disease_by_name and disease.name != data.name:
            raise DiseaseAlreadyExistsException()
        disease_by_code = await self.uow.diseases.get_disease_by_code(disease_code=data.code)
        if disease_by_code and disease.code != data.code:
            raise DiseaseAlreadyExistsException()
        async with self.uow:
            updated_disease = await self.uow.diseases.update_disease(disease=disease, data=data)
        return DiseaseResponseSchema.model_validate(updated_disease)

    async def get_all(self) -> list[DiseaseResponseSchema]:
        diseases = await self.uow.diseases.get_all_diseases()
        if not diseases:
            raise DiseaseNotFoundException()
        return [DiseaseResponseSchema.model_validate(disease) for disease in diseases]

    async def get_by_code(self, disease_code: str) -> DiseaseResponseSchema:
        disease = await self.uow.diseases.get_disease_by_code(disease_code=disease_code)
        if not disease:
            raise DiseaseNotFoundException()
        return DiseaseResponseSchema.model_validate(disease)

    async def get_by_name(self, disease_name: str) -> DiseaseResponseSchema:
        disease = await self.uow.diseases.get_disease_by_name(disease_name=disease_name)
        if not disease:
            raise DiseaseNotFoundException()
        return DiseaseResponseSchema.model_validate(disease)

    async def delete(self, disease_id: int) -> None:
        disease = await self.uow.diseases.get_disease_by_id(disease_id=disease_id)
        if not disease:
            raise DiseaseNotFoundException()
        async with self.uow:
            await self.uow.diseases.delete_disease(disease=disease)
        return None


