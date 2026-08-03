from fastapi import APIRouter, Depends, status

from app.appointments.dependencies import get_appointment_service
from app.appointments.schemas.appointment import (
    AppointmentCreateSchema,
    AppointmentResponseSchema,
)
from app.appointments.services.appointment import AppointmentService
from app.auth.dependencies import get_current_user
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.pagination.schemas import PaginatedResponse, PaginationParams
from common.permissions.checks import check_role
from common.types import ID

router = APIRouter(tags=["Appointments"], prefix="/appointments")


@router.get(
    path="/{appointment_id}",
    summary="Get appointment by ID",
    description=(
        "Returns appointment information by its identifier.\n\n"
        "Available for:\n"
        " - Patient (only their own appointments)\n"
        " - Doctor (only their own appointments)\n"
        " - Admin (any appointments)"
    ),
    status_code=status.HTTP_200_OK,
    response_model=AppointmentResponseSchema,
)
async def get_by_id(
    appointment_id: ID,
    appointment_service: AppointmentService = Depends(get_appointment_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.PATIENT,
        UserRole.DOCTOR,
        UserRole.ADMIN,
    )
    appointment = await appointment_service.get_appointment_by_id(
        appointment_id=appointment_id, current_user=current_user
    )
    return AppointmentResponseSchema.model_validate(appointment)


@router.post(
    path="",
    summary="Create appointment",
    description=(
        "Creates a new appointment.\n\nAvailable for patients and administrators."
    ),
    status_code=status.HTTP_201_CREATED,
    response_model=AppointmentResponseSchema,
)
async def create_appointment(
    data: AppointmentCreateSchema,
    appointment_service: AppointmentService = Depends(get_appointment_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.PATIENT,
        UserRole.ADMIN,
    )
    appointment = await appointment_service.create_appointment(data=data)
    return appointment


@router.get(
    path="/me/past",
    summary="Get past appointments",
    description=(
        "Returns a paginated list of completed appointments.\n\n"
        "for the currently authenticated user"
    ),
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[AppointmentResponseSchema],
)
async def get_past_appointments_by_current_user(
    pagination: PaginationParams = Depends(),
    appointment_service: AppointmentService = Depends(get_appointment_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.PATIENT,
        UserRole.DOCTOR,
        UserRole.ADMIN,
    )
    return await appointment_service.get_past_apps_by_user_id(
        user_id=current_user.id,
        pagination=pagination,
    )


@router.get(
    path="/me/future",
    summary="Get future appointments",
    description=(
        "Returns a paginated list of future appointments.\n\n"
        "for the currently authenticated user"
    ),
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[AppointmentResponseSchema],
)
async def get_future_appointments_by_current_user(
    pagination: PaginationParams = Depends(),
    appointment_service: AppointmentService = Depends(get_appointment_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.PATIENT,
        UserRole.DOCTOR,
        UserRole.ADMIN,
    )
    return await appointment_service.get_future_apps_by_user_id(
        user_id=current_user.id,
        pagination=pagination,
    )


@router.delete(
    path="/{appointment_id}",
    summary="Delete appointment",
    description=(
        "Deletes an appointment by its identifier\n\nAvailable only for administrators."
    ),
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    appointment_id: ID,
    current_user: User = Depends(get_current_user),
    appointment_service: AppointmentService = Depends(get_appointment_service),
):
    check_role(
        current_user,
        UserRole.ADMIN,
    )
    return await appointment_service.delete(appointment_id)
