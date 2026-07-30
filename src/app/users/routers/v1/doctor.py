from fastapi import APIRouter, Depends, status

from app.users.schemas.specialization import SpecializationResponseSchema
from common.types import Email, ID
from app.users.dependencies import get_user_service

from app.users.services.user import UserService
from app.users.schemas.user import (
    DoctorCreateSchema,
    DoctorResponseSchema,
    DoctorUpdateSchema,
)
from app.auth.dependencies import get_current_user
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.permissions.checks import check_role

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


@router.get(
    path="/admin/all",
    status_code=status.HTTP_200_OK,
    response_model=list[DoctorResponseSchema],
)
async def get_doctors_for_admin(
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN)
    return await user_service.get_all_doctors_for_admin()


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=DoctorResponseSchema,
)
async def create_doctor(
    data: DoctorCreateSchema,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> DoctorResponseSchema:
    check_role(current_user, UserRole.ADMIN)
    return await user_service.create_doctor(data=data)


@router.get(
    path="/admin/id/{doctor_id}",
    status_code=status.HTTP_200_OK,
    response_model=DoctorResponseSchema,
)
async def get_doctor_by_id_for_admin(
    doctor_id: ID,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> DoctorResponseSchema:
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await user_service.get_doctor_by_id_for_admin(
        doctor_id=doctor_id,
    )


@router.get(
    path="/id/{doctor_id}",
    status_code=status.HTTP_200_OK,
    response_model=DoctorResponseSchema,
)
async def get_doctor_by_id(
    doctor_id: ID,
    user_service: UserService = Depends(get_user_service),
) -> DoctorResponseSchema:
    doctor = await user_service.get_doctor_by_id(doctor_id=doctor_id)
    return doctor


@router.get(
    path="/email/{doctor_email}",
    status_code=status.HTTP_200_OK,
    response_model=DoctorResponseSchema,
)
async def get_doctor_by_email(
    doctor_email: Email,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> DoctorResponseSchema:
    doctor = await user_service.get_doctor_by_email(
        email=doctor_email,
        current_user=current_user,
    )
    return doctor


@router.get(
    path="/specialization/{specialization_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[DoctorResponseSchema],
)
async def get_by_specialization_id(
    specialization_id: ID,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_doctors_by_specialization_id(
        specialization_id=specialization_id
    )


@router.get(
    path="/admin/specialization/{specialization_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[DoctorResponseSchema],
)
async def get_by_specialization_id_for_admin(
    specialization_id: ID,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN)
    return await user_service.get_doctors_by_specialization_id(
        specialization_id=specialization_id, admin=True
    )


@router.put(
    path="/{doctor_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=DoctorResponseSchema,
)
async def update(
    doctor_id: ID,
    data: DoctorUpdateSchema,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return await user_service.update_doctor(
        doctor_id=doctor_id,
        data=data,
        current_user=current_user,
    )


@router.patch(
    path="/{doctor_id}/deactivate",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=DoctorResponseSchema,
)
async def deactivate(
    doctor_id: ID,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN)
    return await user_service.deactivate_doctor(doctor_id=doctor_id)
