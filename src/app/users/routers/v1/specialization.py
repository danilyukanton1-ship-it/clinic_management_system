from fastapi import APIRouter, Depends, status

from common.pagination.schemas import PaginationParams, PaginatedResponse
from common.types import Email, ID
from app.users.services.specialization import SpecializationService

from app.users.dependencies import get_specialization_service

from app.users.schemas.specialization import (
    SpecializationResponseSchema,
    SpecializationCreateSchema,
    SpecializationUpdateSchema,
)
from app.auth.dependencies import get_current_user
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.permissions.checks import check_role

router = APIRouter(prefix="/specializations", tags=["Specializations"])


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[SpecializationResponseSchema],
)
async def get_all(
    pagination: PaginationParams = Depends(),
    specializations_service: SpecializationService = Depends(
        get_specialization_service
    ),
) -> PaginatedResponse[SpecializationResponseSchema]:
    return await specializations_service.get_all(
        pagination=pagination,
    )


@router.get(
    path="/id/{specialization_id}",
    status_code=status.HTTP_200_OK,
    response_model=SpecializationResponseSchema,
)
async def get_by_id(
    specialization_id: ID,
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
    return await specialization_service.get_by_name(
        specialization_name=specialization_name
    )


@router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=SpecializationResponseSchema,
)
async def create(
    specialization: SpecializationCreateSchema,
    specialization_service: SpecializationService = Depends(get_specialization_service),
    current_user: User = Depends(get_current_user),
) -> SpecializationResponseSchema:
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await specialization_service.create(data=specialization)


@router.delete(
    path="/{specialization_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    specialization_id: int,
    specialization_service: SpecializationService = Depends(get_specialization_service),
    current_user: User = Depends(get_current_user),
) -> None:
    check_role(
        current_user,
        UserRole.ADMIN,
    )
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
    current_user: User = Depends(get_current_user),
) -> SpecializationResponseSchema:
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await specialization_service.update(
        specialization_id=specialization_id,
        data=data,
    )
