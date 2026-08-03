from sqlalchemy.ext.asyncio import AsyncSession

from app.appointments.exceptions.appointment import AppointmentNotFoundException
from app.medical_records.exceptions.drug import DrugNotFoundException
from app.medical_records.exceptions.prescription import PrescriptionNotFoundException
from app.medical_records.exceptions.prescription_items import (
    PrescriptionItemNotFoundException,
)
from app.medical_records.policy.prescription_item import PrescriptionItemPolicy
from app.medical_records.schemas.prescription_item import (
    PrescriptionItemCreateSchema,
    PrescriptionItemResponseSchema,
    PrescriptionItemUpdateSchema,
)
from app.users.models.user import User
from common.pagination.schemas import PaginatedResponse, PaginationParams
from common.pagination.utils import build_paginated_response
from db.unit_of_work import UnitOfWork


class PrescriptionItemService:
    def __init__(self, session: AsyncSession):
        self.policy = PrescriptionItemPolicy()
        self.uow = UnitOfWork(session=session)

    async def get_by_prescription_id(
        self, prescription_id: int, current_user: User, pagination: PaginationParams
    ) -> PaginatedResponse[PrescriptionItemResponseSchema]:
        prescription_items = await self.uow.prescription_items.get_prescription_items_by_prescription_id_with_pagination(
            prescription_id=prescription_id, pagination=pagination
        )
        if prescription_items.items:
            appointment = (
                await self.uow.appointments.get_appointment_by_prescription_item_id(
                    prescription_item_id=prescription_items.items[0].id
                )
            )
            if not appointment:
                raise AppointmentNotFoundException()
            self.policy.can_view(user=current_user, appointment=appointment)
        return build_paginated_response(
            items=prescription_items.items,
            total=prescription_items.total,
            pagination=pagination,
            schema=PrescriptionItemResponseSchema,
        )

    async def get_by_id(
        self, prescription_item_id: int, current_user: User
    ) -> PrescriptionItemResponseSchema:
        prescription_item = (
            await self.uow.prescription_items.get_prescription_item_by_id(
                prescription_item_id=prescription_item_id
            )
        )
        if not prescription_item:
            raise PrescriptionItemNotFoundException()
        appointment = (
            await self.uow.appointments.get_appointment_by_prescription_item_id(
                prescription_item_id=prescription_item.id
            )
        )
        if not appointment:
            raise AppointmentNotFoundException()
        self.policy.can_view(user=current_user, appointment=appointment)
        return PrescriptionItemResponseSchema.model_validate(prescription_item)

    async def update(
        self,
        prescription_item_id: int,
        data: PrescriptionItemUpdateSchema,
        current_user: User,
    ) -> PrescriptionItemResponseSchema:
        async with self.uow:
            prescription_item = (
                await self.uow.prescription_items.get_prescription_item_by_id(
                    prescription_item_id=prescription_item_id
                )
            )
            if not prescription_item:
                raise PrescriptionItemNotFoundException()
            appointment = (
                await self.uow.appointments.get_appointment_by_prescription_item_id(
                    prescription_item_id=prescription_item.id
                )
            )
            if not appointment:
                raise AppointmentNotFoundException()
            self.policy.can_update(user=current_user, appointment=appointment)
            updated_prescription_item = (
                await self.uow.prescription_items.update_prescription_item(
                    prescription_item=prescription_item, data=data
                )
            )
            return PrescriptionItemResponseSchema.model_validate(
                updated_prescription_item
            )

    async def delete(self, prescription_item_id: int, current_user: User) -> None:
        async with self.uow:
            prescription_item = (
                await self.uow.prescription_items.get_prescription_item_by_id(
                    prescription_item_id=prescription_item_id
                )
            )
            if not prescription_item:
                raise PrescriptionItemNotFoundException()
            appointment = (
                await self.uow.appointments.get_appointment_by_prescription_item_id(
                    prescription_item_id=prescription_item.id
                )
            )
            if not appointment:
                raise AppointmentNotFoundException()
            self.policy.can_delete(user=current_user, appointment=appointment)
            await self.uow.prescription_items.delete_prescription_item(
                prescription_item=prescription_item
            )

    async def create(
        self, data: PrescriptionItemCreateSchema
    ) -> PrescriptionItemResponseSchema:
        async with self.uow:
            prescription = await self.uow.prescriptions.get_prescription_by_id(
                prescription_id=data.prescription_id
            )
            if not prescription:
                raise PrescriptionNotFoundException()
            drug = await self.uow.drugs.get_drug_by_id(drug_id=data.drug_id)
            if not drug:
                raise DrugNotFoundException()
            prescription_item = (
                await self.uow.prescription_items.create_prescription_item(data=data)
            )
        return PrescriptionItemResponseSchema.model_validate(prescription_item)
