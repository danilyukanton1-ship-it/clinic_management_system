from fastapi import APIRouter, Depends, status

from app.medical_records.dependencies import get_prescription_item_service
from app.medical_records.schemas.prescription_item import PrescriptionItemResponseSchema, PrescriptionItemUpdateSchema, \
    PrescriptionItemCreateSchema
from app.medical_records.services.prescription_item import PrescriptionItemService

router = APIRouter(
    prefix="/prescription_item",
    tags=["Prescription items"],
)

@router.get(
    path="/prescription/{prescription_id}",
    status_code=status.HTTP_200_OK,
    response_model=PrescriptionItemResponseSchema,
)
async def get_by_prescription_id(
    prescription_id: int,
    prescription_item_service: PrescriptionItemService = Depends(get_prescription_item_service),
):
    return await prescription_item_service.get_by_prescription_id(prescription_id)

@router.get(
    path="/{prescription_item_id}",
    status_code=status.HTTP_200_OK,
    response_model=PrescriptionItemResponseSchema,
)
async def get_by_id(
    prescription_item_id: int,
    prescription_item_service: PrescriptionItemService = Depends(get_prescription_item_service),
):
    return await prescription_item_service.get_by_id(prescription_item_id)

@router.put(
    path="/{prescription_item_id}",
    response_model=PrescriptionItemResponseSchema,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update(
    prescription_item_id: int,
    data: PrescriptionItemUpdateSchema,
    prescription_item_service: PrescriptionItemService = Depends(get_prescription_item_service),
):
    return await prescription_item_service.update(prescription_item_id=prescription_item_id, data=data)

@router.delete(
    path="/{prescription_item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(
    prescription_item_id: int,
    prescription_item_service: PrescriptionItemService = Depends(get_prescription_item_service),
):
    return await prescription_item_service.delete(prescription_item_id)


@router.post(
    path="/",
    response_model=PrescriptionItemResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    data: PrescriptionItemCreateSchema,
    prescription_service: PrescriptionItemService = Depends(get_prescription_item_service),
):
    return await prescription_service.create(data)