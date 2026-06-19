from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_session
from app.appoinments.services.appointment import AppointmentService

async def get_appointment_service(
    session: AsyncSession = Depends(get_session)
):
    return AppointmentService(session)
