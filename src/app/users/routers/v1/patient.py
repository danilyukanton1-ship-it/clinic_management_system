from fastapi import APIRouter, Depends, status

from app.users.dependencies import get_user_service

from app.users.services.user import UserService
from app.users.schemas.user import PatientResponseSchema, PatientCreateSchema
from common.enums.user_role import UserRole

router = APIRouter(
    prefix="/patient",
    tags=["Patients"],
)

@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[PatientResponseSchema],
)
async def get_patients(
    user_service: UserService = Depends(get_user_service),
) -> list[PatientResponseSchema]:
    patients = await user_service.get_all_patients()
    return patients

@router.post(
    path='',
    status_code=status.HTTP_201_CREATED,
    response_model=PatientResponseSchema,
)
async def create_patient(
    patient: PatientCreateSchema,
    user_service: UserService = Depends(get_user_service),
) -> PatientResponseSchema:
    patient = await user_service.create_patient(patient)
    return patient

@router.get(
    path='/id/{patient_id}',
    status_code=status.HTTP_200_OK,
    response_model=PatientResponseSchema,
)
async def get_patient_by_id(
    patient_id: int,
    user_service: UserService = Depends(get_user_service),
) -> PatientResponseSchema:
    patient = await user_service.get_user_by_id(user_role=UserRole.PATIENT, user_id=patient_id)
    return patient

@router.get(
    path='/email/{patient_email}',
    status_code=status.HTTP_200_OK,
    response_model=PatientResponseSchema,
)
async def get_patient_by_email(
    patient_email: str,
    user_service: UserService = Depends(get_user_service),
) -> PatientResponseSchema:
    patient = await user_service.get_user_by_email(user_role=UserRole.PATIENT, user_email=patient_email)
    return patient