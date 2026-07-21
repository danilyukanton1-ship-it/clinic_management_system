from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.appointments.services.attachment import AttachmentService
from core.dependencies import get_session
from app.appointments.services.appointment import AppointmentService

async def get_appointment_service(
    session: AsyncSession = Depends(get_session)
):
    return AppointmentService(session)

async def get_attachment_service(
    session: AsyncSession = Depends(get_session)
):
    return AttachmentService(session)
