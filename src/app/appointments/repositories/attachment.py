from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.appointments.models.attachment import Attachment
from app.appointments.schemas.attachment import (
    AttachmentCreateSchema,
    AttachmentUpdateSchema,
)


class AttachmentRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_attachment(
        self, data: AttachmentCreateSchema, uploaded_by_id: int
    ) -> Attachment:
        attachment = Attachment(**data.model_dump(), uploaded_by_id=uploaded_by_id)
        self.session.add(attachment)
        await self.session.flush()
        await self.session.refresh(attachment)
        return attachment

    async def get_attachment_by_id(self, attachment_id: int) -> Attachment | None:
        stmt = select(Attachment).where(Attachment.id == attachment_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_attachments_by_appointment_id(
        self, appointment_id: int
    ) -> list[Attachment]:
        stmt = select(Attachment).where(Attachment.appointment_id == appointment_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_attachments_by_patient_id(self, patient_id: int) -> list[Attachment]:
        stmt = select(Attachment).where(Attachment.patient_id == patient_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update_attachment(
        self,
        attachment: Attachment,
        data: AttachmentUpdateSchema,
    ) -> Attachment:
        attachment.filename = data.filename
        attachment.file_path = data.file_path
        attachment.file_mime_type = data.file_mime_type
        attachment.file_size = data.file_size
        await self.session.flush()
        await self.session.refresh(attachment)
        return attachment

    async def delete_attachment(self, attachment: Attachment) -> None:
        await self.session.delete(attachment)
        await self.session.flush()
        return None
