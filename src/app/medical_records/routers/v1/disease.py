from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.medical_records.dependencies import get_disease_service
from app.medical_records.schemas.disease import (
    DiseaseCreateSchema,
    DiseaseResponseSchema,
    DiseaseUpdateSchema,
)
from app.medical_records.services.disease import DiseaseService
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.pagination.schemas import PaginatedResponse, PaginationParams
from common.permissions.checks import check_role
from common.types import ID

router = APIRouter(
    tags=["Diseases"],
    prefix="/diseases",
)


@router.get(
    path="/all",
    summary="Get all diseases",
    description=(
        "Returns a paginated list of all diseases.\n\n"
        "Available for doctors and administrators."
    ),
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[DiseaseResponseSchema],
)
async def get_all(
    pagination: PaginationParams = Depends(),
    disease_service: DiseaseService = Depends(get_disease_service),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN, UserRole.DOCTOR)
    return await disease_service.get_all(
        pagination=pagination,
    )


@router.get(
    path="/code/{disease_code}",
    summary="Get disease by code",
    description=(
        "Returns a disease by its unique code.\n\n"
        "Available for doctors and administrators."
    ),
    status_code=status.HTTP_200_OK,
    response_model=DiseaseResponseSchema,
)
async def get_by_code(
    disease_code: str,
    disease_service: DiseaseService = Depends(get_disease_service),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN, UserRole.DOCTOR)
    return await disease_service.get_by_code(disease_code=disease_code)


@router.get(
    path="/name/{disease_name}",
    summary="Get disease by name",
    description=(
        "Returns a disease by its name.\n\nAvailable for doctors and administrators."
    ),
    status_code=status.HTTP_200_OK,
    response_model=DiseaseResponseSchema,
)
async def get_by_name(
    disease_name: str,
    disease_service: DiseaseService = Depends(get_disease_service),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN, UserRole.DOCTOR)
    return await disease_service.get_by_name(disease_name=disease_name)


@router.post(
    path="",
    summary="Create disease",
    description=("Creates a new disease.\n\nAvailable for administrators."),
    status_code=status.HTTP_201_CREATED,
    response_model=DiseaseResponseSchema,
)
async def create(
    data: DiseaseCreateSchema,
    disease_service: DiseaseService = Depends(get_disease_service),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN)
    return await disease_service.create(data=data)


@router.put(
    path="/{disease_id}",
    summary="Update disease",
    description=("Updates an existing disease.\n\nAvailable for administrators."),
    status_code=status.HTTP_202_ACCEPTED,
    response_model=DiseaseResponseSchema,
)
async def update(
    disease_id: ID,
    data: DiseaseUpdateSchema,
    disease_service: DiseaseService = Depends(get_disease_service),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN)
    return await disease_service.update(disease_id=disease_id, data=data)


@router.delete(
    path="/{disease_id}",
    summary="Delete disease",
    description=("Deletes a disease.\n\nAvailable for administrators."),
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    disease_id: ID,
    disease_service: DiseaseService = Depends(get_disease_service),
    current_user: User = Depends(get_current_user),
):
    check_role(current_user, UserRole.ADMIN)
    return await disease_service.delete(disease_id=disease_id)
