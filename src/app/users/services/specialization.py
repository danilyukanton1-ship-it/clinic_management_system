from sqlalchemy.ext.asyncio import AsyncSession

from app.users.exceptions.specialization import (
    SpecializationAlreadyExistsException,
    SpecializationNotFoundException,
)
from app.users.schemas.specialization import (
    SpecializationCreateSchema,
    SpecializationResponseSchema,
    SpecializationUpdateSchema,
)
from common.pagination.schemas import PaginatedResponse, PaginationParams
from common.pagination.utils import build_paginated_response
from db.unit_of_work import UnitOfWork


class SpecializationService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(self.session)

    async def get_by_id(self, specialization_id: int) -> SpecializationResponseSchema:
        specialization = await self.uow.specializations.get_specialization_by_id(
            specialization_id=specialization_id
        )
        if not specialization:
            raise SpecializationNotFoundException()
        return SpecializationResponseSchema.model_validate(specialization)

    async def get_by_name(
        self, specialization_name: str
    ) -> SpecializationResponseSchema:
        specialization = await self.uow.specializations.get_specialization_by_name(
            specialization_name=specialization_name
        )
        if not specialization:
            raise SpecializationNotFoundException()
        return SpecializationResponseSchema.model_validate(specialization)

    async def get_all(
        self, pagination: PaginationParams
    ) -> PaginatedResponse[SpecializationResponseSchema]:
        specializations = await self.uow.specializations.get_all_specializations(
            pagination=pagination
        )
        return build_paginated_response(
            items=specializations.items,
            total=specializations.total,
            pagination=pagination,
            schema=SpecializationResponseSchema,
        )

    async def create(
        self, data: SpecializationCreateSchema
    ) -> SpecializationResponseSchema:
        async with self.uow:
            if await self.uow.specializations.get_specialization_by_name(
                specialization_name=data.name
            ):
                raise SpecializationAlreadyExistsException()
            specialization = await self.uow.specializations.create_specialization(
                data=data
            )
        return SpecializationResponseSchema.model_validate(specialization)

    async def delete(self, specialization_id: int) -> None:
        async with self.uow:
            specialization = await self.uow.specializations.get_specialization_by_id(
                specialization_id=specialization_id
            )
            if not specialization:
                raise SpecializationNotFoundException()
            await self.uow.specializations.delete_specialization(
                specialization=specialization
            )

    async def update(
        self, specialization_id: int, data: SpecializationUpdateSchema
    ) -> SpecializationResponseSchema:
        async with self.uow:
            specialization = await self.uow.specializations.get_specialization_by_id(
                specialization_id=specialization_id
            )
            if not specialization:
                raise SpecializationNotFoundException()
            name_specialization = (
                await self.uow.specializations.get_specialization_by_name(
                    specialization_name=data.name
                )
            )
            if name_specialization and data.name != specialization.name:
                raise SpecializationAlreadyExistsException()
            updated_specialization = (
                await self.uow.specializations.update_specialization(
                    specialization=specialization, data=data
                )
            )
        return SpecializationResponseSchema.model_validate(updated_specialization)
