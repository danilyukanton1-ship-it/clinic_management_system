from fastapi import APIRouter, Depends, status

from app.users.dependencies import get_user_service

from app.users.services.user import UserService
from app.users.schemas.user import DoctorCreateSchema, DoctorResponseSchema, PatientResponseSchema, PatientCreateSchema

from common.enums.user_role import UserRole

router = APIRouter(
    prefix="/doctor",
    tags=["Doctors"],
)

@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[DoctorResponseSchema],
)
async def get_doctors(
    user_service: UserService = Depends(get_user_service),
) -> list[DoctorResponseSchema]:
    doctors = await user_service.get_all_doctors()
    return doctors

@router.post(
    path='',
    status_code=status.HTTP_201_CREATED,
    response_model=DoctorResponseSchema,
)
async def create_doctor(
    doctor: DoctorCreateSchema,
    user_service: UserService = Depends(get_user_service),
) -> DoctorResponseSchema:
    doctor = await user_service.create_doctor(doctor)
    return doctor

@router.get(
    path='/id/{doctor_id}',
    status_code=status.HTTP_200_OK,
    response_model=DoctorResponseSchema,
)
async def get_doctor_by_id(
    doctor_id: int,
    user_service: UserService = Depends(get_user_service),
) -> DoctorResponseSchema:
    doctor = await user_service.get_user_by_id(user_role=UserRole.DOCTOR, user_id=doctor_id)
    return doctor

@router.get(
    path='/email/{doctor_email}',
    status_code=status.HTTP_200_OK,
    response_model=DoctorResponseSchema,
)
async def get_doctor_by_email(
    doctor_email: str,
    user_service: UserService = Depends(get_user_service),
) -> DoctorResponseSchema:
    doctor = await user_service.get_user_by_email(user_role=UserRole.DOCTOR, user_email=doctor_email)
    return doctor
