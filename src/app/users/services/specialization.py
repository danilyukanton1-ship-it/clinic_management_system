from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models.specialization import Specialization

from app.users.repositories.specialization import SpecializationRepository

from app.users.schemas.specialization import SpecializationCreateSchema

from app.users.exceptions.specialization import SpecializationNotFoundException, SpecializationAlreadyExistsException


class SpecializationService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.specialization_repo = SpecializationRepository(session)

    async def get_specialization(self, specialization_id: int) -> Specialization:
        specialization = await self.specialization_repo.get_by_id(specialization_id)
        if not specialization:
            raise SpecializationNotFoundException()
        return specialization

    async def create(self, specialization: SpecializationCreateSchema) -> Specialization:
        specialization_name = specialization.name
        if await self.specialization_repo.get_by_name(specialization_name):
            raise SpecializationAlreadyExistsException()
        specialization = await self.specialization_repo.create(specialization)
        return specialization

    async def delete(self, specialization_id: int) -> None:
        if await self.specialization_repo.get_by_id(specialization_id) is None:
            raise SpecializationNotFoundException()
        return await self.specialization_repo.delete(specialization_id)