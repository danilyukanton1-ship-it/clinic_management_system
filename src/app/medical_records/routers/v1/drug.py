from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.medical_records.dependencies import get_drug_service
from app.medical_records.schemas.drug import (
    DrugCreateSchema,
    DrugResponseSchema,
    DrugUpdateSchema,
)
from app.medical_records.services.drug import DrugService
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.pagination.schemas import PaginatedResponse, PaginationParams
from common.permissions.checks import check_role
from common.types import ID

router = APIRouter(
    prefix="/drugs",
    tags=["Drugs"],
)


@router.get(
    path="/all",
    summary="Get all drugs",
    description=(
        "Returns a paginated list of all drugs.\n\n"
        "Available for doctors and administrators."
    ),
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[DrugResponseSchema],
)
async def get_drugs(
    pagination: PaginationParams = Depends(),
    drug_service: DrugService = Depends(get_drug_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
        UserRole.DOCTOR,
    )
    return await drug_service.get_all(pagination=pagination)


@router.get(
    path="/{drug_id}",
    summary="Get drug by ID",
    description=(
        "Returns a drug by its unique identifier.\n\n"
        "Available for doctors and administrators."
    ),
    status_code=status.HTTP_200_OK,
    response_model=DrugResponseSchema,
)
async def get_by_id(
    drug_id: ID,
    drug_service: DrugService = Depends(get_drug_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
        UserRole.DOCTOR,
    )
    return await drug_service.get_by_id(drug_id=drug_id)


@router.get(
    path="/name/{drug_name}",
    summary="Get drug by name",
    description=(
        "Returns a drug by its name.\n\nAvailable for doctors and administrators."
    ),
    status_code=status.HTTP_200_OK,
    response_model=DrugResponseSchema,
)
async def get_by_name(
    drug_name: str,
    drug_service: DrugService = Depends(get_drug_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
        UserRole.DOCTOR,
    )
    return await drug_service.get_by_name(name=drug_name)


@router.post(
    path="",
    summary="Create drug",
    description=("Creates a new drug.\n\nAvailable for administrators."),
    status_code=status.HTTP_201_CREATED,
    response_model=DrugResponseSchema,
)
async def create(
    data: DrugCreateSchema,
    drug_service: DrugService = Depends(get_drug_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await drug_service.create(data=data)


@router.put(
    path="/{drug_id}",
    summary="Update drug",
    description=("Updates an existing drug.\n\nAvailable for administrators."),
    status_code=status.HTTP_202_ACCEPTED,
    response_model=DrugResponseSchema,
)
async def update(
    drug_id: ID,
    data: DrugUpdateSchema,
    drug_service: DrugService = Depends(get_drug_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await drug_service.update(drug_id=drug_id, data=data)


@router.delete(
    path="/{drug_id}",
    summary="Delete drug",
    description=("Deletes a drug.\n\nAvailable for administrators."),
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    drug_id: ID,
    drug_service: DrugService = Depends(get_drug_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await drug_service.delete(drug_id=drug_id)
