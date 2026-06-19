from fastapi import APIRouter, Depends, status

from app.appoinments.dependencies import get_appointment_service

from app.appoinments.services.appointment import AppointmentService
from app.appoinments.schemas.appointment import AppointmentCreateSchema, AppointmentResponseSchema

router = APIRouter()

@router.post(
      path="/appointment",
      tags=["Appointments"],
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
      path='/appointment',
      tags=["Appointments"],
      status_code=status.HTTP_200_OK,
      response_model= list[AppointmentResponseSchema],
)
async def get_all_appointments(
      appointment_service: AppointmentService = Depends(get_appointment_service),
):
      appointments = await appointment_service.get_all_appointments()
      return appointments