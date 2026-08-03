from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.appointments.exceptions.appointment import (
    AppointmentNotFoundException,
    AppointmentRelatesToDifferentPatientException,
)
from app.appointments.exceptions.attachment import AttachmentDoesNotExistException
from app.appointments.policy.attachments import AttachmentPolicy
from app.appointments.schemas.attachment import (
    AttachmentCreateSchema,
    AttachmentResponseSchema,
    AttachmentSchema,
    AttachmentUpdateSchema,
)
from app.users.exceptions.user import UserNotFoundException
from app.users.models.user import User
from common.pagination.schemas import PaginatedResponse, PaginationParams
from common.pagination.utils import build_paginated_response
from db.unit_of_work import UnitOfWork
from infrastructure.storages.interface import StorageInterface
from infrastructure.storages.schemas import DownloadUrl


class AttachmentService:
    def __init__(self, session: AsyncSession, storage: StorageInterface) -> None:
        self.policy = AttachmentPolicy()
        self.uow = UnitOfWork(session)
        self.storage = storage

    async def create(
        self, data: AttachmentCreateSchema, file: UploadFile, current_user: User
    ) -> AttachmentResponseSchema:
        async with self.uow:
            patient = await self.uow.users.get_patient_by_id(patient_id=data.patient_id)
            if not patient:
                raise UserNotFoundException()
            appointment = await self.uow.appointments.get_appointment_by_id(
                appointment_id=data.appointment_id
            )
            if not appointment:
                raise AppointmentNotFoundException()
            if appointment.patient_id != patient.id:
                raise AppointmentRelatesToDifferentPatientException()
            stored_file = await self.storage.save(file=file)
            attachment_data = AttachmentSchema(
                filename=file.filename,
                file_path=stored_file.key,
                file_size=stored_file.size,
                file_mime_type=stored_file.content_type,
                patient_id=patient.id,
                appointment_id=appointment.id,
            )
            attachment = await self.uow.attachments.create_attachment(
                data=attachment_data, uploaded_by_id=current_user.id
            )
        return AttachmentResponseSchema.model_validate(attachment)

    async def update(
        self, attachment_id: int, data: AttachmentUpdateSchema, current_user: User
    ) -> AttachmentResponseSchema:
        async with self.uow:
            attachment = await self.uow.attachments.get_attachment_by_id(
                attachment_id=attachment_id
            )
            if not attachment:
                raise AttachmentDoesNotExistException()
            self.policy.can_update(user=current_user, attachment=attachment)
            updated_attachment = await self.uow.attachments.update_attachment(
                attachment=attachment, data=data
            )
        return AttachmentResponseSchema.model_validate(updated_attachment)

    async def delete(self, attachment_id: int, current_user: User) -> None:
        async with self.uow:
            attachment = await self.uow.attachments.get_attachment_by_id(
                attachment_id=attachment_id
            )
            if not attachment:
                raise AttachmentDoesNotExistException()
            self.policy.can_delete(user=current_user, attachment=attachment)
            await self.storage.delete(attachment.file_path)
            await self.uow.attachments.delete_attachment(attachment=attachment)

    async def get_by_id(self, attachment_id: int) -> AttachmentResponseSchema:
        attachment = await self.uow.attachments.get_attachment_by_id(
            attachment_id=attachment_id
        )
        if not attachment:
            raise AttachmentDoesNotExistException()
        return AttachmentResponseSchema.model_validate(attachment)

    async def get_by_appointment_id(
        self, appointment_id: int, pagination: PaginationParams
    ) -> PaginatedResponse[AttachmentResponseSchema]:
        attachments = await self.uow.attachments.get_attachments_by_appointment_id(
            appointment_id=appointment_id,
            pagination=pagination,
        )
        return build_paginated_response(
            items=attachments.items,
            total=attachments.total,
            pagination=pagination,
            schema=AttachmentResponseSchema,
        )

    async def get_by_patient_id(
        self, patient_id: int, pagination: PaginationParams
    ) -> PaginatedResponse[AttachmentResponseSchema]:
        attachments = await self.uow.attachments.get_attachments_by_patient_id(
            patient_id=patient_id, pagination=pagination
        )
        return build_paginated_response(
            items=attachments.items,
            total=attachments.total,
            pagination=pagination,
            schema=AttachmentResponseSchema,
        )

    async def get_download_url(self, attachment_id: int) -> DownloadUrl:
        attachment = await self.uow.attachments.get_attachment_by_id(
            attachment_id=attachment_id
        )
        if not attachment:
            raise AttachmentDoesNotExistException()
        return await self.storage.get_download_url(attachment.file_path)
