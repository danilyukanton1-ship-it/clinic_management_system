from fastapi import APIRouter, Depends, status

from common.pagination.schemas import PaginatedResponse, PaginationParams
from common.types import Email, ID, Phone
from app.users.dependencies import get_user_service

from app.users.services.user import UserService
from app.users.schemas.user import PatientResponseSchema, PatientUpdateSchema
from app.auth.dependencies import get_current_user
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.permissions.checks import check_role

router = APIRouter(
    prefix="/patients",
    tags=["Patients"],
)


@router.get(
    path="/all",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[PatientResponseSchema],
)
async def get_patients(
    pagination: PaginationParams = Depends(),
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> PaginatedResponse[PatientResponseSchema]:
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await user_service.get_all_patients(pagination=pagination)


@router.get(
    path="/id/{patient_id}",
    status_code=status.HTTP_200_OK,
    response_model=PatientResponseSchema,
)
async def get_patient_by_id(
    patient_id: ID,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> PatientResponseSchema:
    return await user_service.get_patient_by_id(
        patient_id=patient_id,
        current_user=current_user,
    )


@router.get(
    path="/admin/id/{patient_id}",
    status_code=status.HTTP_200_OK,
    response_model=PatientResponseSchema,
)
async def get_patient_by_id_for_admin(
    patient_id: ID,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> PatientResponseSchema:
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await user_service.get_patient_by_id(
        patient_id=patient_id,
        current_user=current_user,
        admin=True,
    )


@router.get(
    path="/email/{patient_email}",
    status_code=status.HTTP_200_OK,
    response_model=PatientResponseSchema,
)
async def get_patient_by_email(
    patient_email: Email,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> PatientResponseSchema:
    return await user_service.get_patient_by_email(
        email=patient_email,
        current_user=current_user,
    )


@router.get(
    path="/phone/{phone_number}",
    status_code=status.HTTP_200_OK,
    response_model=PatientResponseSchema,
)
async def get_patient_by_phone(
    phone_number: Phone,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return await user_service.get_patient_by_phone(
        phone=phone_number,
        current_user=current_user,
    )


@router.put(
    path="/{patient_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=PatientResponseSchema,
)
async def update(
    patient_id: ID,
    data: PatientUpdateSchema,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    return await user_service.update_patient(
        patient_id=patient_id,
        data=data,
        current_user=current_user,
    )


@router.patch(
    path="/{patient_id}/deactivate",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=PatientResponseSchema,
)
async def deactivate(
    patient_id: ID,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await user_service.deactivate_patient(
        patient_id=patient_id,
    )
