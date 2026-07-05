from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.medical_records.schemas.prescription_item import PrescriptionItemCreateSchema, PrescriptionItemUpdateSchema

from app.medical_records.models.prescription_item import PrescriptionItem

class PrescriptionItemRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_prescription_item(self, data: PrescriptionItemCreateSchema):
        prescription_item = PrescriptionItem(
            prescription_id=data.prescription_id,
            drug_id=data.drug_id,
            dosage=data.dosage,
            duration_days=data.duration_days,
            frequency=data.frequency,
        )
        self.session.add(prescription_item)
        await self.session.flush()
        await self.session.refresh(prescription_item)
        return prescription_item

    async def get_prescription_items_by_prescription_id(self, prescription_id: int) -> list[PrescriptionItem]:
        stmt = (
            select(PrescriptionItem)
            .where(PrescriptionItem.prescription_id == prescription_id)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_prescription_item_by_id(self, prescription_item_id: int) -> PrescriptionItem | None:
        stmt = (
            select(PrescriptionItem)
            .where(PrescriptionItem.id == prescription_item_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def update_prescription_item(self, prescription_item: PrescriptionItem, data: PrescriptionItemUpdateSchema) -> PrescriptionItem:
        prescription_item.drug_id = data.drug_id
        prescription_item.dosage = data.dosage
        prescription_item.duration_days = data.duration_days
        prescription_item.frequency = data.frequency
        await self.session.flush()
        await self.session.refresh(prescription_item)
        return prescription_item

    async def delete_prescription_item(self, prescription_item: PrescriptionItem) -> None:
        await self.session.delete(prescription_item)
        await self.session.flush()
        await self.session.refresh(prescription_item)
        return None
