from fastapi import APIRouter, Depends, status
from app.medical_records.dependencies import get_diagnosis_service
from app.medical_records.schemas.diagnosis import DiagnosisCreateSchema, DiagnosisUpdateSchema, DiagnosisResponseSchema
from app.medical_records.services.diagnosis import DiagnosisService

router = APIRouter(
    prefix="/diagnoses",
    tags=["Diagnoses"],
)

@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[DiagnosisResponseSchema],
)
async def get_all(
    diagnosis_service: DiagnosisService = Depends(get_diagnosis_service),
):
    return await diagnosis_service.get_all()

@router.get(
    path="/id/{diagnosis_id}",
    status_code=status.HTTP_200_OK,
    response_model=DiagnosisResponseSchema,
)
async def get_by_id(
    diagnosis_id: int,
    diagnosis_service: DiagnosisService = Depends(get_diagnosis_service),
):
    return await diagnosis_service.get_by_id(diagnosis_id)

@router.get(
    path="/prescription/{prescription_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[DiagnosisResponseSchema],
)
async def get_by_prescription_id(
    prescription_id: int,
    diagnosis_service: DiagnosisService = Depends(get_diagnosis_service),
):
    return await diagnosis_service.get_by_prescription_id(prescription_id=prescription_id)

@router.get(
    path="/disease/{disease_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[DiagnosisResponseSchema],
)
async def get_by_diagnosis_id(
    disease_id: int,
    diagnosis_service: DiagnosisService = Depends(get_diagnosis_service),
):
    return await diagnosis_service.get_by_disease_id(disease_id=disease_id)

@router.put(
    path="/{diagnosis_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=DiagnosisResponseSchema,
)
async def update(
    diagnosis_id: int,
    data: DiagnosisUpdateSchema,
    diagnosis_service: DiagnosisService = Depends(get_diagnosis_service),
):
    return await diagnosis_service.update(diagnosis_id=diagnosis_id, data=data)

@router.delete(
    path="/{diagnosis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    diagnosis_id: int,
    diagnosis_service: DiagnosisService = Depends(get_diagnosis_service),
):
    return await diagnosis_service.delete(diagnosis_id=diagnosis_id)

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=DiagnosisResponseSchema,
)
async def create(
    data: DiagnosisCreateSchema,
    diagnosis_service: DiagnosisService = Depends(get_diagnosis_service),
):
    return await diagnosis_service.create(data=data)