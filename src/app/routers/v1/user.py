from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_session

from app.servicies.user import UserService
from app.schemas.user import DoctorCreateSchema, DoctorResponseSchema, PatientResponseSchema, PatientCreateSchema

from app.enums.user_role import UserRole

router = APIRouter()

@router.get(
    path="/doctor",
    tags=["Doctors"],
    status_code=status.HTTP_200_OK,
    response_model=DoctorResponseSchema,
)
async def get_doctors(
    session: AsyncSession = Depends(get_session),
) -> list[DoctorResponseSchema]:
    user_service = UserService(session)
    doctors = await user_service.get_all_doctors()
    return doctors

@router.post(
    path='/doctor',
    tags=["Doctors"],
    status_code=status.HTTP_201_CREATED,
    response_model=DoctorResponseSchema,
)
async def create_doctor(
    doctor: DoctorCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    user_service = UserService(session)
    doctor = await user_service.create_doctor(doctor)
    return doctor

@router.post(
    path='/patient',
    tags=["Patients"],
    status_code=status.HTTP_201_CREATED,
    response_model=PatientResponseSchema,
)
async def create_patient(
    patient: PatientCreateSchema,
    session: AsyncSession = Depends(get_session),
):
    user_service = UserService(session)
    patient = await user_service.create_patient(patient)
    return patient

@router.get(
    path='/patient/{patient_id}',
    tags=["Patients"],
    status_code=status.HTTP_200_OK,
    response_model=PatientResponseSchema,
)
async def get_patient(
    user: int | str,
    session: AsyncSession = Depends(get_session),
):
    user_service = UserService(session)
    patient = await user_service.get_user_by_id_or_email(user_role=UserRole.PATIENT, user=user)
    return patient

@router.get(
    path='/doctor/{doctor_id}',
    tags=["Doctors"],
    status_code=status.HTTP_200_OK,
    response_model=DoctorResponseSchema,
)
async def get_doctor(
    user: int | str,
    session: AsyncSession = Depends(get_session),
):
    user_service = UserService(session)
    doctor = await user_service.get_user_by_id_or_email(user_role=UserRole.DOCTOR, user=user)
    return doctor