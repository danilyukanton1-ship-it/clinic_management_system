from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies import get_session
from app.medical_records.services.disease import DiseaseService

async def get_disease_service(
    session: AsyncSession = Depends(get_session)
):
    return DiseaseService(session)
