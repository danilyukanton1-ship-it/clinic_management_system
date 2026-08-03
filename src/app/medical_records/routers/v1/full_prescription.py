from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.medical_records.dependencies import get_full_prescription_service
from app.medical_records.schemas.prescription import (
    FullPrescriptionCreateSchema,
    FullPrescriptionResponseSchema,
)
from app.medical_records.services.full_prescription import FullPrescriptionService
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.permissions.checks import check_role
from common.types import ID

router = APIRouter(
    prefix="/full_prescriptions",
    tags=["Full prescriptions"],
)


@router.post(
    path="/",
    summary="Create full prescription",
    description=(
        "Creates a complete prescription, including diagnoses, prescriptions items"
        "Available for doctors and administrators."
    ),
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
    summary="Get full prescription by appointment",
    description=(
        "Returns the complete prescription associated with the specified appointment.\n\n"
        "Available for:\n"
        " - Patient (only their own prescriptions)\n"
        " - Doctor (any prescriptions)\n"
        " - Admin (any prescriptions)"
    ),
    response_model=FullPrescriptionResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_by_appointment_id(
    appointment_id: ID,
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
    summary="Get full prescription by ID",
    description=(
        "Returns a complete prescription by its unique identifier.\n\n"
        "Available for:\n"
        " - Patient (only their own prescriptions)\n"
        " - Doctor (any prescriptions)\n"
        " - Admin (any prescriptions)"
    ),
    response_model=FullPrescriptionResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_by_prescription_id(
    prescription_id: ID,
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
    summary="Delete full prescription",
    description=(
        "Deletes a complete prescription, including all related entities.\n\n"
        "Available for the assigned doctor and administrators."
    ),
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_by_id(
    prescription_id: ID,
    prescription_service: FullPrescriptionService = Depends(
        get_full_prescription_service
    ),
    current_user: User = Depends(get_current_user),
):

    return await prescription_service.delete_full_prescription(
        prescription_id=prescription_id, current_user=current_user
    )
