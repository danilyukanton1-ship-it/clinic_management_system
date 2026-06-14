from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.specialization import Specialization


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

