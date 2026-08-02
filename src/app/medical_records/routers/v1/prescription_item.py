from fastapi import APIRouter, Depends, status

from common.pagination.schemas import PaginationParams, PaginatedResponse
from common.types import ID
from app.medical_records.dependencies import get_prescription_item_service
from app.medical_records.schemas.prescription_item import (
    PrescriptionItemResponseSchema,
    PrescriptionItemUpdateSchema,
    PrescriptionItemCreateSchema,
)
from app.medical_records.services.prescription_item import PrescriptionItemService
from app.auth.dependencies import get_current_user
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.permissions.checks import check_role

router = APIRouter(
    prefix="/prescription_items",
    tags=["Prescription items"],
)


@router.get(
    path="/prescription/{prescription_id}",
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


@router.delete(path="/{prescription_item_id}", status_code=status.HTTP_204_NO_CONTENT)
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
