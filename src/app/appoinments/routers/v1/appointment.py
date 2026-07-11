from fastapi import APIRouter, Depends, status

from app.appoinments.dependencies import get_appointment_service

from app.appoinments.services.appointment import AppointmentService
from app.appoinments.schemas.appointment import AppointmentCreateSchema, AppointmentResponseSchema
from app.auth.dependencies import get_current_user
from app.users.models.user import User
router = APIRouter(tags=["Appointments"], prefix="/appointments")

@router.post(
      path="/",
      status_code=status.HTTP_201_CREATED,
      response_model= AppointmentResponseSchema,
)
async def create_appointment(
      appointment: AppointmentCreateSchema,
      appointment_service: AppointmentService = Depends(get_appointment_service),
):
      appointment = await appointment_service.create_appointment(appointment)
      return appointment

@router.get(
      path='/',
      status_code=status.HTTP_200_OK,
      response_model= list[AppointmentResponseSchema],
)
async def get_all_appointments(
      appointment_service: AppointmentService = Depends(get_appointment_service),
):
      appointments = await appointment_service.get_all_appointments()
      return appointments

@router.get(
      path='/past/current_user',
      status_code=status.HTTP_200_OK,
      response_model= list[AppointmentResponseSchema],
)
async def get_past_appointments_by_current_user(
      user: User = Depends(get_current_user),
      appointment_service: AppointmentService = Depends(get_appointment_service)
):
      past_apps = appointment_service.get_past_apps_by_user_id(user_id=user.id)
      return past_apps

@router.get(
      path="/future/current_user",
      status_code=status.HTTP_200_OK,
      response_model= list[AppointmentResponseSchema],
)
async def get_future_appointments_by_current_user(
      user: User = Depends(get_current_user),
      appointment_service: AppointmentService = Depends(get_appointment_service),
):
      future_apps = appointment_service.get_future_apps_by_user_id(user_id=user.id)
      return future_apps