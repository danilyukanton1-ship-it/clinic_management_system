from sqlalchemy.ext.asyncio import AsyncSession
from app.medical_records.schemas.drug import DrugCreateSchema, DrugUpdateSchema
from app.medical_records.models.drug import Drug
from db.unit_of_work import UnitOfWork

class DrugService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(session=session)

    async def create(self, data: DrugCreateSchema) -> Drug:
        async with self.uow:
            drug = await self.uow.drugs.create_drug(data)
        return drug

    async def update(self, drug_id: int, data: DrugUpdateSchema) -> Drug:
        drug = await self.uow.drugs.get_drug_by_id(drug_id=drug_id)
        async with self.uow:
            drug = await self.uow.drugs.update_drug(drug=drug, data=data)
        return drug

    async def get_all(self) -> list[Drug]:
        drugs = await self.uow.drugs.get_all_drugs()
        return drugs

    async def get_by_name(self, name: str) -> Drug:
        drug = await self.uow.drugs.get_drug_by_name(name)
        return drug

    async def delete(self, drug_id: int) -> None:
        drug = await self.uow.drugs.get_drug_by_id(drug_id=drug_id)
        async with self.uow:
            await self.uow.drugs.delete_drug(drug=drug)
        return None
