from sqlalchemy.ext.asyncio import AsyncSession

from app.medical_records.exceptions.drug import DrugNotFoundException
from app.medical_records.exceptions.prescription import PrescriptionNotFoundException
from app.medical_records.exceptions.prescription_items import PrescriptionItemNotFoundException
from app.medical_records.schemas.prescription_item import PrescriptionItemUpdateSchema, PrescriptionItemResponseSchema, \
    PrescriptionItemCreateSchema
from db.unit_of_work import UnitOfWork


class PrescriptionItemService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(session=self.session)

    async def get_by_prescription_id(self, prescription_id: int) -> PrescriptionItemResponseSchema:
        prescription_item = await self.uow.prescription_items.get_prescription_items_by_prescription_id(prescription_id=prescription_id)
        if not prescription_item:
            raise PrescriptionItemNotFoundException()
        return PrescriptionItemResponseSchema.model_validate(prescription_item)

    async def get_by_id(self, prescription_item_id: int) -> PrescriptionItemResponseSchema:
        prescription_item = await self.uow.prescription_items.get_prescription_item_by_id(prescription_item_id=prescription_item_id)
        if not prescription_item:
            raise PrescriptionItemNotFoundException()
        return PrescriptionItemResponseSchema.model_validate(prescription_item)

    async def update(self, prescription_item_id: int, data: PrescriptionItemUpdateSchema) -> PrescriptionItemResponseSchema:
        async with self.uow:
            prescription_item = await self.uow.prescription_items.get_prescription_item_by_id(prescription_item_id=prescription_item_id)
            if not prescription_item:
                raise PrescriptionItemNotFoundException()
            prescription_item = await self.uow.prescription_items.update_prescription_item(prescription_item=prescription_item, data=data)
            return PrescriptionItemResponseSchema.model_validate(prescription_item)

    async def delete(self, prescription_item_id: int) -> None:
        async with self.uow:
            prescription_item = await self.uow.prescription_items.get_prescription_item_by_id(prescription_item_id=prescription_item_id)
            if not prescription_item:
                raise PrescriptionItemNotFoundException()
            await self.uow.prescription_items.delete_prescription_item(prescription_item=prescription_item)
        return None

    async def create(self, data: PrescriptionItemCreateSchema) -> PrescriptionItemResponseSchema:
        async with self.uow:
            prescription = await self.uow.prescriptions.get_prescription_by_id(prescription_id=data.prescription_id)
            if not prescription:
                raise PrescriptionNotFoundException()
            drug = await self.uow.drugs.get_drug_by_id(drug_id=data.drug_id)
            if not drug:
                raise DrugNotFoundException()
            prescription_item = await self.uow.prescription_items.create_prescription_item(data=data)
        return PrescriptionItemResponseSchema.model_validate(prescription_item)



