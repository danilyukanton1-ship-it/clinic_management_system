from fastapi import APIRouter, Depends, status
from app.medical_records.schemas.prescription import (
    FullPrescriptionCreateSchema,
    FullPrescriptionResponseSchema,
)
from app.medical_records.dependencies import get_full_prescription_service
from app.medical_records.services.full_prescription import FullPrescriptionService
from app.auth.dependencies import get_current_user
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.permissions.checks import check_role

router = APIRouter(
    prefix="/full_prescriptions",
    tags=["Full prescriptions"],
)


@router.post(
    path="/",
    response_model=FullPrescriptionResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    data: FullPrescriptionCreateSchema,
    prescription_service: FullPrescriptionService = Depends(
        get_full_prescription_service
    ),
    current_user: User = Depends(get_current_user),
) -> FullPrescriptionResponseSchema:
    check_role(current_user, UserRole.ADMIN, UserRole.DOCTOR)
    return await prescription_service.create_full_prescription(data=data)


@router.get(
    path="/appointment/{appointment_id}",
    response_model=FullPrescriptionResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_by_appointment_id(
    appointment_id: int,
    prescription_service: FullPrescriptionService = Depends(
        get_full_prescription_service
    ),
    current_user: User = Depends(get_current_user),
):
    return await prescription_service.get_full_prescription_by_appointment_id(
        appointment_id=appointment_id,
        current_user=current_user,
    )


@router.get(
    path="/{prescription_id}",
    response_model=FullPrescriptionResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_by_prescription_id(
    prescription_id: int,
    prescription_service: FullPrescriptionService = Depends(
        get_full_prescription_service
    ),
    current_user: User = Depends(get_current_user),
) -> FullPrescriptionResponseSchema:
    return await prescription_service.get_full_prescription_by_prescription_id(
        prescription_id=prescription_id,
        current_user=current_user,
    )


@router.delete(
    path="/{prescription_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_by_id(
    prescription_id: int,
    prescription_service: FullPrescriptionService = Depends(
        get_full_prescription_service
    ),
    current_user: User = Depends(get_current_user),
):

    return await prescription_service.delete_full_prescription(
        prescription_id=prescription_id, current_user=current_user
    )
