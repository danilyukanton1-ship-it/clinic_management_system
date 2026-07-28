from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_session
from app.medical_records.services.disease import DiseaseService
from app.medical_records.services.drug import DrugService
from app.medical_records.services.diagnosis import DiagnosisService
from app.medical_records.services.full_prescription import FullPrescriptionService
from app.medical_records.services.prescription import PrescriptionService
from app.medical_records.services.prescription_item import PrescriptionItemService


async def get_disease_service(session: AsyncSession = Depends(get_session)):
    return DiseaseService(session)


async def get_drug_service(session: AsyncSession = Depends(get_session)):
    return DrugService(session)


async def get_diagnosis_service(session: AsyncSession = Depends(get_session)):
    return DiagnosisService(session)


async def get_full_prescription_service(session: AsyncSession = Depends(get_session)):
    return FullPrescriptionService(session)


async def get_prescription_service(session: AsyncSession = Depends(get_session)):
    return PrescriptionService(session)


async def get_prescription_item_service(session: AsyncSession = Depends(get_session)):
    return PrescriptionItemService(session)
