from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.dependencies import get_session
from app.medical_records.services.disease import DiseaseService
from app.medical_records.services.drug import DrugService
from app.medical_records.services.diagnosis import DiagnosisService

async def get_disease_service(
    session: AsyncSession = Depends(get_session)
):
    return DiseaseService(session)

async def get_drug_service(
    session: AsyncSession = Depends(get_session)
):
    return DrugService(session)


async def get_diagnosis_service(
    session: AsyncSession = Depends(get_session)
):
    return DiagnosisService(session)