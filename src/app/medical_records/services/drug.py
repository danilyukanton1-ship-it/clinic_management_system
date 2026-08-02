from requests import session
from sqlalchemy.ext.asyncio import AsyncSession
from app.medical_records.schemas.drug import (
    DrugCreateSchema,
    DrugUpdateSchema,
    DrugResponseSchema,
)
from app.medical_records.exceptions.drug import (
    DrugAlreadyExistsException,
    DrugNotFoundException,
)
from common.pagination.schemas import PaginatedResponse, PaginationParams
from common.pagination.utils import build_paginated_response
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

    async def get_by_id(self, drug_id: int) -> DrugResponseSchema:
        drug = await self.uow.drugs.get_drug_by_id(drug_id=drug_id)
        if not drug:
            raise DrugNotFoundException
        return DrugResponseSchema.model_validate(drug)

    async def get_all(self, pagination: PaginationParams) -> PaginatedResponse[DrugResponseSchema]:
        drugs = await self.uow.drugs.get_all_drugs(
            pagination=pagination
        )
        return build_paginated_response(
            items=drugs.items,
            total=drugs.total,
            pagination=pagination,
            schema=DrugResponseSchema
        )

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
