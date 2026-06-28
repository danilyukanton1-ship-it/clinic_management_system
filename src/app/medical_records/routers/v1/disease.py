from fastapi import APIRouter, Depends, status
from app.medical_records.dependencies import get_disease_service
from app.medical_records.services.disease import DiseaseService
from app.medical_records.schemas.disease import DiseaseResponseSchema, DiseaseCreateSchema, DiseaseUpdateSchema
router = APIRouter(
    tags=["Diseases"],
    prefix='/disease',
)

@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[DiseaseResponseSchema]
)
async def get_all(
    disease_service: DiseaseService = Depends(get_disease_service),
):
    return await disease_service.get_all()

@router.get(
    path="/code",
    status_code=status.HTTP_200_OK,
    response_model=DiseaseResponseSchema
)
async def get_by_code(
    disease_code: str,
    disease_service: DiseaseService = Depends(get_disease_service)
):
    return await disease_service.get_by_code(disease_code=disease_code)

@router.get(
    path="/name",
    status_code=status.HTTP_200_OK,
    response_model=DiseaseResponseSchema
)
async def get_by_name(
    disease_name: str,
    disease_service: DiseaseService = Depends(get_disease_service)
):
    return await disease_service.get_by_name(name=disease_name)

@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=DiseaseResponseSchema
)
async def create(
    data: DiseaseCreateSchema,
    disease_service: DiseaseService = Depends(get_disease_service)
):
    return await disease_service.create(data=data)

@router.put(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=DiseaseResponseSchema
)
async def update(
    disease_id: int,
    data: DiseaseUpdateSchema,
    disease_service: DiseaseService = Depends(get_disease_service)
):
    return await disease_service.update(disease_id=disease_id, data=data)

@router.delete(
    path="/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    disease_id: int,
    disease_service: DiseaseService = Depends(get_disease_service)
):
    return await disease_service.delete(disease_id=disease_id)
