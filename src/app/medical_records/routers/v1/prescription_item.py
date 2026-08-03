from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.medical_records.dependencies import get_prescription_item_service
from app.medical_records.schemas.prescription_item import (
    PrescriptionItemCreateSchema,
    PrescriptionItemResponseSchema,
    PrescriptionItemUpdateSchema,
)
from app.medical_records.services.prescription_item import PrescriptionItemService
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.pagination.schemas import PaginatedResponse, PaginationParams
from common.permissions.checks import check_role
from common.types import ID

router = APIRouter(
    prefix="/prescription_items",
    tags=["Prescription items"],
)


@router.get(
    path="/prescription/{prescription_id}",
    summary="Get prescription items by prescription ID",
    description=(
        "Returns a paginated list of prescription items associated with the specified prescription.\n\n"
        "Available for:\n"
        "- Patient (only their own prescription items)\n"
        "- Doctor (any prescription items)\n"
        "- Administrator (any prescription items)"
    ),
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[PrescriptionItemResponseSchema],
)
async def get_by_prescription_id(
    prescription_id: ID,
    pagination: PaginationParams = Depends(),
    prescription_item_service: PrescriptionItemService = Depends(
        get_prescription_item_service
    ),
    current_user: User = Depends(get_current_user),
):
    return await prescription_item_service.get_by_prescription_id(
        prescription_id=prescription_id,
        current_user=current_user,
        pagination=pagination,
    )


@router.get(
    path="/{prescription_item_id}",
    summary="Get prescription item by ID",
    description=(
        "Returns a prescription item by its unique identifier.\n\n"
        "Available for:\n"
        "- Patient (only their own prescription items)\n"
        "- Doctor (any prescription items)\n"
        "- Administrator (any prescription items)"
    ),
    status_code=status.HTTP_200_OK,
    response_model=PrescriptionItemResponseSchema,
)
async def get_by_id(
    prescription_item_id: ID,
    prescription_item_service: PrescriptionItemService = Depends(
        get_prescription_item_service
    ),
    current_user: User = Depends(get_current_user),
):
    return await prescription_item_service.get_by_id(
        prescription_item_id=prescription_item_id,
        current_user=current_user,
    )


@router.put(
    path="/{prescription_item_id}",
    summary="Update prescription item",
    description=(
        "Updates an existing prescription item.\n\n"
        "Available for:\n"
        "- Doctor (only prescription items they created)\n"
        "- Administrator (any prescription items)"
    ),
    response_model=PrescriptionItemResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update(
    prescription_item_id: ID,
    data: PrescriptionItemUpdateSchema,
    prescription_item_service: PrescriptionItemService = Depends(
        get_prescription_item_service
    ),
    current_user: User = Depends(get_current_user),
):
    return await prescription_item_service.update(
        prescription_item_id=prescription_item_id,
        data=data,
        current_user=current_user,
    )


@router.delete(
    path="/{prescription_item_id}",
    summary="Delete prescription item",
    description=(
        "Deletes a prescription item.\n\n"
        "Available for:\n"
        "- Doctor (only prescription items they created)\n"
        "- Administrator (any prescription items)"
    ),
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    prescription_item_id: ID,
    prescription_item_service: PrescriptionItemService = Depends(
        get_prescription_item_service
    ),
    current_user: User = Depends(get_current_user),
):
    return await prescription_item_service.delete(
        prescription_item_id=prescription_item_id,
        current_user=current_user,
    )


@router.post(
    path="",
    summary="Create prescription item",
    description=(
        "Creates a new prescription item.\n\nAvailable for:\n- Doctor\n- Administrator"
    ),
    response_model=PrescriptionItemResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    data: PrescriptionItemCreateSchema,
    prescription_service: PrescriptionItemService = Depends(
        get_prescription_item_service
    ),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN, UserRole.DOCTOR)
    return await prescription_service.create(data)
