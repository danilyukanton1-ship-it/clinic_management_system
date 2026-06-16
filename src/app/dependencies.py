from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_session

from app.servicies.specialization import SpecializationService

async def get_specialization_service(
    session: AsyncSession = Depends(get_session)
):
    return SpecializationService(session)