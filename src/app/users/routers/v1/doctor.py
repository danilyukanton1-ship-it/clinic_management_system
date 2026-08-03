from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.users.dependencies import get_user_service
from app.users.models.user import User
from app.users.schemas.user import (
    DoctorCreateSchema,
    DoctorResponseSchema,
    DoctorUpdateSchema,
)
from app.users.services.user import UserService
from common.enums.user_role import UserRole
from common.pagination.schemas import PaginatedResponse, PaginationParams
from common.permissions.checks import check_role
from common.types import ID, Email

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"],
)


@router.get(
    path="/all",
    summary="Get all doctors",
    description=(
        "Returns a paginated list of active doctors.\n\nAvailable for everyone."
    ),
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[DoctorResponseSchema],
)
async def get_doctors(
    pagination: PaginationParams = Depends(),
    user_service: UserService = Depends(get_user_service),
) -> PaginatedResponse[DoctorResponseSchema]:
    doctors = await user_service.get_all_doctors(
        pagination=pagination,
    )
    return doctors


@router.get(
    path="/admin/all",
    summary="Get all doctors (admin)",
    description=(
        "Returns a paginated list of all doctors, including inactive accounts.\n\n"
        "Available for:\n"
        "- Administrator"
    ),
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[DoctorResponseSchema],
)
async def get_doctors_for_admin(
    pagination: PaginationParams = Depends(),
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> PaginatedResponse[DoctorResponseSchema]:
    check_role(current_user, UserRole.ADMIN)
    return await user_service.get_all_doctors_for_admin(pagination=pagination)


@router.post(
    path="",
    summary="Create doctor",
    description=("Creates a new doctor account.\n\nAvailable for:\n- Administrator"),
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
    summary="Get doctor by ID (admin)",
    description=(
        "Returns a doctor account by its unique identifier, including inactive accounts.\n\n"
        "Available for:\n"
        "- Administrator"
    ),
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
    summary="Get doctor by ID",
    description=(
        "Returns a doctor by their unique identifier.\n\nAvailable for everyone."
    ),
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
    summary="Get doctor by email",
    description=(
        "Returns a doctor account by email address.\n\n"
        "Available for:\n"
        "- Doctor (their own account)\n"
        "- Administrator (any doctor account)"
    ),
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
    summary="Get doctors by specialization ID",
    description=(
        "Returns all doctors with the specified specialization.\n\n"
        "Available for everyone."
    ),
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
    summary="Get doctors by specialization ID (admin)",
    description=(
        "Returns all doctors with the specified specialization, including inactive accounts.\n\n"
        "Available for:\n"
        "- Administrator"
    ),
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
    summary="Update doctor",
    description=(
        "Updates an existing doctor account.\n\n"
        "Available for:\n"
        "- Doctor (their own account)\n"
        "- Administrator (any doctor account)"
    ),
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
    summary="Deactivate doctor",
    description=(
        "Deactivates a doctor account without permanently deleting it.\n\n"
        "Available for:\n"
        "- Administrator"
    ),
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
