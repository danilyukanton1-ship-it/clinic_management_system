from fastapi import APIRouter, Depends, status

from app.users.dependencies import get_user_service

from app.users.services.user import UserService
from app.users.schemas.user import PatientResponseSchema, PatientUpdateSchema

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
    return await user_service.get_all_patients()

@router.get(
    path='/id/{patient_id}',
    status_code=status.HTTP_200_OK,
    response_model=PatientResponseSchema,
)
async def get_patient_by_id(
    patient_id: int,
    user_service: UserService = Depends(get_user_service),
) -> PatientResponseSchema:
    return await user_service.get_patient_by_id(patient_id=patient_id)

@router.get(
    path='/email/{patient_email}',
    status_code=status.HTTP_200_OK,
    response_model=PatientResponseSchema,
)
async def get_patient_by_email(
    patient_email: str,
    user_service: UserService = Depends(get_user_service),
) -> PatientResponseSchema:
    return await user_service.get_patient_by_email(email=patient_email)

@router.get(
    path="/phone/{phone_number}",
    status_code=status.HTTP_200_OK,
    response_model=PatientResponseSchema,
)
async def get_patient_by_phone(
    phone: str,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_patient_by_phone(phone=phone)

@router.put(
    path="/{patient_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=PatientResponseSchema,
)
async def update(
    patient_id: int,
    data: PatientUpdateSchema,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.update_patient(patient_id=patient_id, data=data)