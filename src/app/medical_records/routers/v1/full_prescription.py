from fastapi import APIRouter, Depends, status
from app.medical_records.schemas.prescription import FullPrescriptionCreateSchema, FullPrescriptionResponseSchema
from app.medical_records.dependencies import get_full_prescription_service
from app.medical_records.services.full_prescription import FullPrescriptionService

router = APIRouter(
    prefix="/full_prescription",
    tags=["Full prescriptions"],
)

@router.post(
    path="/",
    response_model=FullPrescriptionResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    data: FullPrescriptionCreateSchema,
    prescription_service: FullPrescriptionService = Depends(get_full_prescription_service),
) -> FullPrescriptionResponseSchema:
    return await prescription_service.create_full_prescription(data)

@router.get(
    path="/appointment/{appointment_id}",
    response_model=FullPrescriptionResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_by_appointment_id(
    appointment_id: int,
    prescription_service: FullPrescriptionService = Depends(get_full_prescription_service),
):
    return await prescription_service.get_full_prescription_by_appointment_id(appointment_id=appointment_id)

@router.get(
    path="/{prescription_id}",
    response_model=FullPrescriptionResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_by_prescription_id(
    prescription_id: int,
    prescription_service: FullPrescriptionService = Depends(get_full_prescription_service),
) -> FullPrescriptionResponseSchema:
    return await prescription_service.get_full_prescription_by_prescription_id(prescription_id=prescription_id)

@router.delete(
    path="/{prescription_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_by_id(
    prescription_id: int,
    prescription_service: FullPrescriptionService = Depends(get_full_prescription_service),
):
    return await prescription_service.delete_full_prescription(prescription_id=prescription_id)

