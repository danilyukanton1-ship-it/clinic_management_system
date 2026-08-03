from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.medical_records.dependencies import get_prescription_service
from app.medical_records.schemas.prescription import (
    PrescriptionResponseSchema,
    PrescriptionUpdateSchema,
)
from app.medical_records.services.prescription import PrescriptionService
from app.users.models.user import User
from common.types import ID

router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"],
)


@router.put(
    path="/{prescription_id}",
    summary="Update prescription",
    description=(
        "Updates an existing prescription.\n\n"
        "Available for the assigned doctor and administrators."
    ),
    response_model=PrescriptionResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update(
    prescription_id: ID,
    data: PrescriptionUpdateSchema,
    prescription_service: PrescriptionService = Depends(get_prescription_service),
    current_user: User = Depends(get_current_user),
):
    return await prescription_service.update(
        prescription_id=prescription_id, data=data, current_user=current_user
    )
