from fastapi import APIRouter, Depends, status

from app.users.dependencies import get_user_service

from app.users.services.user import UserService
from app.users.schemas.user import DoctorCreateSchema, DoctorResponseSchema, DoctorUpdateSchema

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
)

@router.get(
    path="/all",
    status_code=status.HTTP_200_OK,
    response_model=list[DoctorResponseSchema],
)
async def get_doctors(
    user_service: UserService = Depends(get_user_service),
) -> list[DoctorResponseSchema]:
    doctors = await user_service.get_all_doctors()
    return doctors

@router.post(
    path='/',
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
    doctor = await user_service.get_doctor_by_id(doctor_id=doctor_id)
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
    doctor = await user_service.get_doctor_by_email(email=doctor_email)
    return doctor


@router.get(
    path='/specialization/{specialization_id}',
    status_code=status.HTTP_200_OK,
    response_model=list[DoctorResponseSchema],
)
async def get_by_specialization_id(
    specialization_id: int,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_doctors_by_specialization_id(specialization_id=specialization_id)

@router.put(
    path="/{doctor_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=DoctorResponseSchema,
)
async def update(
    doctor_id: int,
    data: DoctorUpdateSchema,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.update_doctor(doctor_id=doctor_id, data=data)