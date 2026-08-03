from sqlalchemy import select

from app.appointments.models.attachment import Attachment
from app.appointments.schemas.attachment import AttachmentSchema, AttachmentUpdateSchema
from common.pagination.schemas import PaginationParams, PaginationResult
from core.repository import BaseRepository


class AttachmentRepository(BaseRepository):
    async def create_attachment(
        self, data: AttachmentSchema, uploaded_by_id: int
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
        self, appointment_id: int, pagination: PaginationParams
    ) -> PaginationResult[Attachment]:
        stmt = select(Attachment).where(Attachment.appointment_id == appointment_id)
        return await self.paginate(
            stmt=stmt,
            pagination=pagination,
        )

    async def get_attachments_by_patient_id(
        self, patient_id: int, pagination: PaginationParams
    ) -> PaginationResult[Attachment]:
        stmt = select(Attachment).where(Attachment.patient_id == patient_id)
        return await self.paginate(
            stmt=stmt,
            pagination=pagination,
        )

    async def update_attachment(
        self,
        attachment: Attachment,
        data: AttachmentUpdateSchema,
    ) -> Attachment:
        attachment.filename = data.filename
        await self.session.flush()
        await self.session.refresh(attachment)
        return attachment

    async def delete_attachment(self, attachment: Attachment) -> None:
        await self.session.delete(attachment)
