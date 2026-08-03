from sqlalchemy import select

from app.users.models.specialization import Specialization
from app.users.schemas.specialization import (
    SpecializationCreateSchema,
    SpecializationUpdateSchema,
)
from common.pagination.schemas import PaginationParams, PaginationResult
from core.repository import BaseRepository


class SpecializationRepository(BaseRepository):

    async def get_all_specializations(
        self, pagination: PaginationParams
    ) -> PaginationResult[Specialization]:
        stmt = select(Specialization)
        return await self.paginate(
            stmt=stmt,
            pagination=pagination,
        )

    async def get_specialization_by_id(
        self, specialization_id: int
    ) -> Specialization | None:
        stmt = select(Specialization).where(Specialization.id == specialization_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_specialization_by_name(
        self, specialization_name: str
    ) -> Specialization | None:
        stmt = select(Specialization).where(Specialization.name == specialization_name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_specialization(
        self, specialization: Specialization, data: SpecializationUpdateSchema
    ) -> Specialization:
        specialization.name = data.name
        specialization.description = data.description
        await self.session.flush()
        await self.session.refresh(specialization)
        return specialization

    async def create_specialization(
        self, data: SpecializationCreateSchema
    ) -> Specialization:
        specialization = Specialization(
            name=data.name,
            description=data.description,
        )
        self.session.add(specialization)
        await self.session.commit()
        await self.session.refresh(specialization)
        return specialization

    async def delete_specialization(self, specialization: Specialization) -> None:
        await self.session.delete(specialization)
        await self.session.flush()
