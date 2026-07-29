from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.appointments.services.attachment import AttachmentService
from core.dependencies import get_session
from app.appointments.services.appointment import AppointmentService
from infrastructure.storages.services import MinioStorageService
from infrastructure.dependencies import get_minio_service


async def get_appointment_service(session: AsyncSession = Depends(get_session)):
    return AppointmentService(session)


async def get_attachment_service(
    session: AsyncSession = Depends(get_session),
    storage: MinioStorageService = Depends(get_minio_service),
):
    return AttachmentService(session=session, storage=storage)
