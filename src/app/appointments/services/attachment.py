from sqlalchemy.ext.asyncio import AsyncSession

from app.appointments.schemas.attachment import AttachmentCreateSchema, AttachmentUpdateSchema, AttachmentResponseSchema
from app.appointments.exceptions.attachment import AttachmentDoesNotExistException
from app.users.models.user import User
from app.appointments.policy.attachments import AttachmentPolicy

from db.unit_of_work import UnitOfWork

class AttachmentService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.policy = AttachmentPolicy()
        self.uow = UnitOfWork(self.session)

    async def create(self, data: AttachmentCreateSchema, current_user: User) -> AttachmentResponseSchema:
        async with self.uow:

            attachment = await self.uow.attachments.create_attachment(data=data, uploaded_by_id=current_user.id)
        return AttachmentResponseSchema.model_validate(attachment)

    async def update(
            self,
            attachment_id: int,
            data: AttachmentUpdateSchema,
            current_user: User
    ) -> AttachmentResponseSchema:
        async with self.uow:
            attachment = await self.uow.attachments.get_attachment_by_id(attachment_id=attachment_id)
            if not attachment:
                raise AttachmentDoesNotExistException()
            self.policy.can_update(current_user, attachment)
            updated_attachment = await self.uow.attachments.update_attachment(attachment=attachment, data=data)
        return AttachmentResponseSchema.model_validate(updated_attachment)

    async def delete(self, attachment_id: int, current_user: User) -> None:
        async with self.uow:
            attachment = await self.uow.attachments.get_attachment_by_id(attachment_id=attachment_id)
            if not attachment:
                raise AttachmentDoesNotExistException()
            self.policy.can_delete(current_user, attachment)
            await self.uow.attachments.delete_attachment(attachment=attachment)
        return None

    async def get_by_id(self, attachment_id: int, current_user: User) -> AttachmentResponseSchema:
        attachment = await self.uow.attachments.get_attachment_by_id(attachment_id=attachment_id)
        if not attachment:
            raise AttachmentDoesNotExistException()
        self.policy.can_view(current_user, attachment)
        return AttachmentResponseSchema.model_validate(attachment)

    async def get_by_appointment_id(self, appointment_id: int, current_user: User) -> list[AttachmentResponseSchema]:
        attachments = await self.uow.attachments.get_attachments_by_appointment_id(appointment_id=appointment_id)
        for attachment in attachments:
            self.policy.can_view(current_user, attachment)
        return [AttachmentResponseSchema.model_validate(attachment) for attachment in attachments]

    async def get_by_patient_id(self, patient_id: int, current_user: User) -> list[AttachmentResponseSchema]:
        attachments = await self.uow.attachments.get_attachments_by_patient_id(patient_id=patient_id)
        for attachment in attachments:
            self.policy.can_view(current_user, attachment)
        return [AttachmentResponseSchema.model_validate(attachment) for attachment in attachments]