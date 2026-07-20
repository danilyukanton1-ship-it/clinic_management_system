from fastapi import APIRouter, Depends, status

from app.users.services.specialization import SpecializationService

from app.users.dependencies import get_specialization_service

from app.users.schemas.specialization import SpecializationResponseSchema, SpecializationCreateSchema, \
    SpecializationUpdateSchema

router = APIRouter(prefix="/specializations",tags=["Specializations"])

@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[SpecializationResponseSchema],
)
async def get_all(
    specializations_service: SpecializationService = Depends(get_specialization_service),
) -> list[SpecializationResponseSchema]:
    return await specializations_service.get_all()

@router.get(
    path="/id/{specialization_id}",
    status_code=status.HTTP_200_OK,
    response_model=SpecializationResponseSchema,
)
async def get_by_id(
    specialization_id: int,
    specialization_service: SpecializationService = Depends(get_specialization_service),
) -> SpecializationResponseSchema:
    return await specialization_service.get_by_id(specialization_id=specialization_id)

@router.get(
    path="/name/{specialization_name}",
    status_code=status.HTTP_200_OK,
    response_model=SpecializationResponseSchema,
)
async def get_by_name(
    specialization_name: str,
    specialization_service: SpecializationService = Depends(get_specialization_service),
) -> SpecializationResponseSchema:
    return await specialization_service.get_by_name(specialization_name=specialization_name)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=SpecializationResponseSchema,
)
async def create(
    specialization: SpecializationCreateSchema,
    specialization_service: SpecializationService = Depends(get_specialization_service),
) -> SpecializationResponseSchema:
    return await specialization_service.create(data=specialization)

@router.delete(
    path="/{specialization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    specialization_id: int,
    specialization_service: SpecializationService = Depends(get_specialization_service),
) -> None:
    return await specialization_service.delete(specialization_id=specialization_id)

@router.put(
    path="/{specialization_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=SpecializationResponseSchema,
)
async def update(
    specialization_id: int,
    data: SpecializationUpdateSchema,
    specialization_service: SpecializationService = Depends(get_specialization_service),
) -> SpecializationResponseSchema:
    return await specialization_service.update(
        specialization_id=specialization_id,
        data=data,
    )