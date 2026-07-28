from sqlalchemy.ext.asyncio import AsyncSession
from app.medical_records.schemas.drug import DrugCreateSchema, DrugUpdateSchema, DrugResponseSchema
from app.medical_records.exceptions.drug import DrugAlreadyExistsException, DrugNotFoundException
from db.unit_of_work import UnitOfWork

class DrugService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(session=session)

    async def create(self, data: DrugCreateSchema) -> DrugResponseSchema:
        drug_by_name = await self.uow.drugs.get_drug_by_name(drug_name=data.name)
        if drug_by_name:
            raise DrugAlreadyExistsException()
        async with self.uow:
            drug = await self.uow.drugs.create_drug(data=data)
        return DrugResponseSchema.model_validate(drug)

    async def update(self, drug_id: int, data: DrugUpdateSchema) -> DrugResponseSchema:
        drug = await self.uow.drugs.get_drug_by_id(drug_id=drug_id)
        if not drug:
            raise DrugNotFoundException()
        drug_by_name = await self.uow.drugs.get_drug_by_name(drug_name=data.name)
        if drug_by_name and drug.name != data.name:
            raise DrugAlreadyExistsException()
        async with self.uow:
            drug = await self.uow.drugs.update_drug(drug=drug, data=data)
        return DrugResponseSchema.model_validate(drug)

    async def get_all(self) -> list[DrugResponseSchema]:
        drugs = await self.uow.drugs.get_all_drugs()
        if not drugs:
            raise DrugNotFoundException()
        return [DrugResponseSchema.model_validate(drug) for drug in drugs]

    async def get_by_name(self, name: str) -> DrugResponseSchema:
        drug = await self.uow.drugs.get_drug_by_name(drug_name=name)
        if not drug:
            raise DrugNotFoundException()
        return DrugResponseSchema.model_validate(drug)

    async def delete(self, drug_id: int) -> None:
        drug = await self.uow.drugs.get_drug_by_id(drug_id=drug_id)
        if not drug:
            raise DrugNotFoundException()
        async with self.uow:
            await self.uow.drugs.delete_drug(drug=drug)
        return None
