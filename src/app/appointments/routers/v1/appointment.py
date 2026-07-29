from fastapi import APIRouter, Depends, status
from common.types import ID
from app.appointments.dependencies import get_appointment_service
from app.appointments.services.appointment import AppointmentService
from app.appointments.schemas.appointment import (
    AppointmentCreateSchema,
    AppointmentResponseSchema,
)
from app.auth.dependencies import get_current_user
from app.users.models.user import User
from common.enums.user_role import UserRole
from common.permissions.checks import check_role

router = APIRouter(tags=["Appointments"], prefix="/appointments")


@router.get(
    path="/{appointment_id}",
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
    status_code=status.HTTP_200_OK,
    response_model=list[AppointmentResponseSchema],
)
async def get_past_appointments_by_current_user(
    user: User = Depends(get_current_user),
    appointment_service: AppointmentService = Depends(get_appointment_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.PATIENT,
        UserRole.DOCTOR,
        UserRole.ADMIN,
    )
    past_apps = await appointment_service.get_past_apps_by_user_id(user_id=user.id)
    return past_apps


@router.get(
    path="/me/future",
    status_code=status.HTTP_200_OK,
    response_model=list[AppointmentResponseSchema],
)
async def get_future_appointments_by_current_user(
    user: User = Depends(get_current_user),
    appointment_service: AppointmentService = Depends(get_appointment_service),
    current_user: User = Depends(get_current_user),
):
    check_role(
        current_user,
        UserRole.PATIENT,
        UserRole.DOCTOR,
        UserRole.ADMIN,
    )
    future_apps = await appointment_service.get_future_apps_by_user_id(user_id=user.id)
    return future_apps


@router.delete(
    path="/{appointment_id}",
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
