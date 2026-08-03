from fastapi import APIRouter, Depends, status

from app.auth.dependencies import get_current_user
from app.users.dependencies import get_user_service
from app.users.models.user import User
from app.users.schemas.user import (
    AdminCreateSchema,
    AdminResponseSchema,
    AdminUpdateSchema,
)
from app.users.services.user import UserService
from common.enums.user_role import UserRole
from common.pagination.schemas import PaginatedResponse, PaginationParams
from common.permissions.checks import check_role
from common.types import ID

router = APIRouter(
    prefix="/admins",
    tags=["Admins"],
)


@router.post(
    path="",
    summary="Create administrator",
    description=(
        "Creates a new administrator account.\n\nAvailable for:\n- Administrator"
    ),
    status_code=status.HTTP_201_CREATED,
    response_model=AdminResponseSchema,
)
async def create(
    data: AdminCreateSchema,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await user_service.create_admin(data=data)


@router.get(
    path="/all",
    summary="Get all administrators",
    description=(
        "Returns a paginated list of administrator accounts.\n\n"
        "Available for:\n"
        "- Administrator"
    ),
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[AdminResponseSchema],
)
async def get_all(
    pagination: PaginationParams = Depends(),
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
) -> PaginatedResponse[AdminResponseSchema]:
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await user_service.get_all_admins(pagination=pagination)


@router.get(
    path="/{admin_id}",
    summary="Get administrator by ID",
    description=(
        "Returns an administrator account by its unique identifier.\n\n"
        "Available for:\n"
        "- Administrator"
    ),
    status_code=status.HTTP_200_OK,
    response_model=AdminResponseSchema,
)
async def get_admin(
    admin_id: ID,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await user_service.get_admin_by_id(admin_id=admin_id)


@router.put(
    path="/{admin_id}",
    summary="Update administrator",
    description=(
        "Updates an existing administrator account.\n\nAvailable for:\n- Administrator"
    ),
    status_code=status.HTTP_202_ACCEPTED,
    response_model=AdminResponseSchema,
)
async def update(
    admin_id: ID,
    data: AdminUpdateSchema,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await user_service.update_admin(data=data, admin_id=admin_id)


@router.patch(
    path="/{admin_id}/deactivate",
    summary="Deactivate administrator",
    description=(
        "Deactivates an administrator account without permanently deleting it.\n\n"
        "Available for:\n"
        "- Administrator"
    ),
    status_code=status.HTTP_202_ACCEPTED,
    response_model=AdminResponseSchema,
)
async def deactivate(
    admin_id: ID,
    user_service: UserService = Depends(get_user_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await user_service.deactivate_admin(admin_id=admin_id)
