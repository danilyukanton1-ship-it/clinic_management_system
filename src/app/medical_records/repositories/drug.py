from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.medical_records.schemas.drug import DrugCreateSchema, DrugUpdateSchema
from app.medical_records.models.drug import Drug

class DrugRepository:

    def __init__(self, session: AsyncSession):
        self.session = session



    async def create_drug(self, data: DrugCreateSchema) -> Drug:
        drug = Drug(
            name=data.name,
            international_name=data.international_name,
            dosage_form=data.dosage_form,
            strength=data.strength,
            description=data.description,
        )
        self.session.add(drug)
        await self.session.flush()
        await self.session.refresh(drug)
        return drug

    async def get_all_drugs(self) -> list[Drug]:
        stmt = (
            select(Drug)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_drug_by_id(self, drug_id: int) -> Drug:
        stmt = (
            select(Drug)
            .where(Drug.id==drug_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_drug_by_name(self, drug_name: str) -> Drug:
        stmt = (
            select(Drug)
            .where(Drug.name==drug_name)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_drug(self, drug: Drug, data: DrugUpdateSchema) -> Drug:
        drug.name = data.name
        drug.international_name = data.international_name
        drug.dosage_form = data.dosage_form
        drug.strength = data.strength
        drug.description = data.description
        await self.session.flush()
        await self.session.refresh(drug)
        return drug

    async def delete_drug(self, drug: Drug) -> None:
        await self.session.delete(drug)
        return None
    