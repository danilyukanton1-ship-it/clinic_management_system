from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.specialization import Specialization

from app.schemas.specialization import SpecializationCreateSchema


class SpecializationRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, specialization_id: int) -> Specialization:
        stmt = (
            select(Specialization)
            .where(Specialization.id == specialization_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, specialization_name: str) -> Specialization:
        stmt = (
            select(Specialization)
            .where(Specialization.name == specialization_name)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, specialization: SpecializationCreateSchema) -> Specialization:
        specialization = Specialization(
            name=specialization.name,
            description=specialization.description,
        )
        self.session.add(specialization)
        await self.session.commit()
        await self.session.refresh(specialization)
        return specialization

    async def delete(self, specialization_id: int) -> None:
        specialization = await self.get_by_id(specialization_id)
        await self.session.delete(specialization)
        return None
