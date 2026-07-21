from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_session

from app.appointments.routers.v1.appointment import router as appointment_router
from app.scheduling.routers.v1.schedule_slot import router as schedule_slot_router
from app.scheduling.routers.v1.schedule import router as schedule_router
from app.users.routers.v1.doctor import router as doctors_router
from app.users.routers.v1.patient import router as patient_router
from app.users.routers.v1.specialization import router as specialization_router
from app.auth.routers.v1.auth import router as auth_router
from app.medical_records.routers.v1.disease import router as disease_router
from app.medical_records.routers.v1.drug import router as drugs_router
from app.medical_records.routers.v1.diagnosis import router as diagnosis_router
from app.medical_records.routers.v1.full_prescription import router as full_prescription_router
from app.medical_records.routers.v1.prescription import router as prescription_router
from app.medical_records.routers.v1.prescription_item import router as prescription_item_router
from app.scheduling.routers.v1.schedule_absence import router as schedule_absence_router
from app.appointments.routers.v1.attachment import router as attachment_router
from app.users.routers.v1.admin import router as admin_router

router = APIRouter()

@router.get(
    path="/health",
    tags=["Health"],
)
async def health():
    return {"status": status.HTTP_200_OK}

@router.get(
    path="/health/db",
    tags=["Health"],
)
async def db_health(session: AsyncSession = Depends(get_session)):
    result = await session.execute(text("SELECT 1"))
    return {"status": result.scalar()}

router.include_router(appointment_router)
router.include_router(schedule_slot_router)
router.include_router(schedule_router)
router.include_router(schedule_absence_router)
router.include_router(doctors_router)
router.include_router(patient_router)
router.include_router(specialization_router)
router.include_router(auth_router)
router.include_router(disease_router)
router.include_router(drugs_router)
router.include_router(diagnosis_router)
router.include_router(full_prescription_router)
router.include_router(prescription_router)
router.include_router(prescription_item_router)
router.include_router(attachment_router)
router.include_router(admin_router)