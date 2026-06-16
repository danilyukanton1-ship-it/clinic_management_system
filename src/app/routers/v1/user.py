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
    response_model=list[DoctorResponseSchema],
)
async def get_doctors(
    session: AsyncSession = Depends(get_session),
) -> list[DoctorResponseSchema]:
    user_service = UserService(session)
    doctors = await user_service.get_all_doctors()
    return doctors

@router.get(
    path="/patient",
    tags=["Patients"],
    status_code=status.HTTP_200_OK,
    response_model=list[PatientResponseSchema],
)
async def get_patients(
    session: AsyncSession = Depends(get_session),
) -> list[PatientResponseSchema]:
    user_service = UserService(session)
    patients = await user_service.get_all_patients()
    return patients

@router.post(
    path='/doctor',
    tags=["Doctors"],
    status_code=status.HTTP_201_CREATED,
    response_model=DoctorResponseSchema,
)
async def create_doctor(
    doctor: DoctorCreateSchema,
    session: AsyncSession = Depends(get_session),
) -> DoctorResponseSchema:
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
) -> PatientResponseSchema:
    user_service = UserService(session)
    patient = await user_service.create_patient(patient)
    return patient

@router.get(
    path='/patient/id/{patient_id}',
    tags=["Patients"],
    status_code=status.HTTP_200_OK,
    response_model=PatientResponseSchema,
)
async def get_patient_by_id(
    patient_id: int,
    session: AsyncSession = Depends(get_session),
) -> PatientResponseSchema:
    user_service = UserService(session)
    patient = await user_service.get_user_by_id(user_role=UserRole.PATIENT, user_id=patient_id)
    return patient

@router.get(
    path='/patient/email/{patient_email}',
    tags=["Patients"],
    status_code=status.HTTP_200_OK,
    response_model=PatientResponseSchema,
)
async def get_patient_by_email(
    patient_email: str,
    session: AsyncSession = Depends(get_session),
) -> PatientResponseSchema:
    user_service = UserService(session)
    patient = await user_service.get_user_by_email(user_role=UserRole.PATIENT, user_email=patient_email)
    return patient

@router.get(
    path='/doctor/id/{doctor_id}',
    tags=["Doctors"],
    status_code=status.HTTP_200_OK,
    response_model=DoctorResponseSchema,
)
async def get_doctor_by_id(
    doctor_id: int,
    session: AsyncSession = Depends(get_session),
) -> DoctorResponseSchema:
    user_service = UserService(session)
    doctor = await user_service.get_user_by_id(user_role=UserRole.DOCTOR, user_id=doctor_id)
    return doctor

@router.get(
    path='/doctor/email/{doctor_email}',
    tags=['Doctors'],
    status_code=status.HTTP_200_OK,
    response_model=DoctorResponseSchema,
)
async def get_doctor_by_email(
    doctor_email: str,
    session: AsyncSession = Depends(get_session),
) -> DoctorResponseSchema:
    user_service = UserService(session)
    doctor = await user_service.get_user_by_email(user_role=UserRole.DOCTOR, user_email=doctor_email)
    return doctor