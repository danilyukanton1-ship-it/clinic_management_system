from fastapi import APIRouter, Depends, status

from app.users.services.specialization import SpecializationService

from app.users.dependencies import get_specialization_service

from app.users.schemas.specialization import SpecializationSchema, SpecializationCreateSchema

router = APIRouter(prefix="specializations",tags=["Specializations"])

@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[SpecializationSchema],
)
async def get_specializations(
    specializations_service: SpecializationService = Depends(get_specialization_service),
) -> list[SpecializationSchema]:
    specializations = await specializations_service.get_all_specializations()
    return specializations

@router.get(
    path="/{specialization_id}",
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
    path="/",
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
    path="/{specialization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_specialization(
    specialization_id: int,
    specialization_service: SpecializationService = Depends(get_specialization_service),
) -> None:
    specialization = await specialization_service.delete(specialization_id)
    return specialization
