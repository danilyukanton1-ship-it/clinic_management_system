from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_session

from app.servicies.appointment import AppointmentService
from app.schemas.appointment import AppointmentCreateSchema, AppointmentResponseSchema

router = APIRouter()

@router.post(
      path="/appointment",
      tags=["Appointments"],
      status_code=status.HTTP_201_CREATED,
      response_model= AppointmentResponseSchema,
)
async def create_appointment(
        appointment: AppointmentCreateSchema,
        session: AsyncSession = Depends(get_session),
):
      appointment_service = AppointmentService(session)
      appointment = await appointment_service.create_appointment(appointment)
      return appointment

@router.get(
      path='/appointment',
      tags=["Appointments"],
      status_code=status.HTTP_200_OK,
      response_model= AppointmentResponseSchema,
)
async def get_all_appointments(
        session: AsyncSession = Depends(get_session),
):
      appointment_service = AppointmentService(session)
      appointments = await appointment_service.get_all_appointments()
      return appointments