from fastapi import APIRouter, Depends, status

from app.servicies.specialization import SpecializationService

from app.dependencies import get_specialization_service

from app.schemas.specialization import SpecializationSchema, SpecializationCreateSchema

router = APIRouter(tags=["Specializations"])

@router.get(
    path="/specialization/{specialization_id}",
    status_code=status.HTTP_200_OK,
    response_model=SpecializationSchema,
)
async def get_specialization_by_id(
    specialization_id: int,
    specialization_service: SpecializationService = Depends(get_specialization_service),
) -> SpecializationSchema:
    specialization = await specialization_service.get_specialization(specialization_id)
    return specialization

@router.post(
    path="/specialization",
    status_code=status.HTTP_201_CREATED,
    response_model=SpecializationSchema,
)
async def create_specialization(
    specialization: SpecializationCreateSchema,
    specialization_service: SpecializationService = Depends(get_specialization_service),
) -> SpecializationSchema:
    specialization = await specialization_service.create(specialization)
    return specialization

@router.delete(
    path="/specialization/{specialization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_specialization(
    specialization_id: int,
    specialization_service: SpecializationService = Depends(get_specialization_service),
) -> None:
    specialization = await specialization_service.delete(specialization_id)
    return specialization
