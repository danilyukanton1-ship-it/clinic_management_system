from sqlalchemy.ext.asyncio import AsyncSession

from app.appoinments.schemas.attachment import AttachmentCreateSchema, AttachmentUpdateSchema, AttachmentResponseSchema
from app.appoinments.exceptions.attachment import AttachmentDoesNotExistException

from db.unit_of_work import UnitOfWork

class AttachmentService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(self.session)

    async def create(self, data: AttachmentCreateSchema, uploaded_by_id: int) -> AttachmentResponseSchema:
        async with self.uow:
            attachment = await self.uow.attachments.create_attachment(data=data, uploaded_by_id=uploaded_by_id)
        return AttachmentResponseSchema.model_validate(attachment)

    async def update(self, attachment_id: int, data: AttachmentUpdateSchema) -> AttachmentResponseSchema:
        async with self.uow:
            attachment = await self.uow.attachments.get_attachment_by_id(attachment_id=attachment_id)
            if not attachment:
                raise AttachmentDoesNotExistException()
            updated_attachment = await self.uow.attachments.update_attachment(attachment=attachment, data=data)
        return AttachmentResponseSchema.model_validate(updated_attachment)

    async def delete(self, attachment_id: int) -> None:
        async with self.uow:
            attachment = await self.uow.attachments.get_attachment_by_id(attachment_id=attachment_id)
            if not attachment:
                raise AttachmentDoesNotExistException()
            await self.uow.attachments.delete_attachment(attachment=attachment)
        return None

    async def get_by_id(self, attachment_id: int) -> AttachmentResponseSchema:
        attachments = await self.uow.attachments.get_attachment_by_id(attachment_id=attachment_id)
        if not attachments:
            raise AttachmentDoesNotExistException()
        return AttachmentResponseSchema.model_validate(attachments)

    async def get_by_appointment_id(self, appointment_id: int) -> list[AttachmentResponseSchema]:
        attachments = await self.uow.attachments.get_attachments_by_appointment_id(appointment_id=appointment_id)
        return [AttachmentResponseSchema.model_validate(attachment) for attachment in attachments]

    async def get_by_patient_id(self, patient_id: int) -> list[AttachmentResponseSchema]:
        attachments = await self.uow.attachments.get_attachments_by_patient_id(patient_id=patient_id)
        return [AttachmentResponseSchema.model_validate(attachment) for attachment in attachments]