from unittest.mock import AsyncMock, MagicMock

import pytest

from app.appointments.exceptions.appointment import (
    AppointmentNotFoundException,
    AppointmentRelatesToDifferentPatientException,
)
from app.appointments.exceptions.attachment import AttachmentDoesNotExistException
from app.appointments.schemas.attachment import (
    AttachmentResponseSchema,
    AttachmentSchema,
)
from app.users.exceptions.user import UserNotFoundException
from common.pagination.schemas import PaginationResult


class TestAttachmentService:
    @pytest.mark.asyncio
    async def test_create_attachment_success(
        self,
        attachment_service,
        current_doctor,
        attachment_create_schema,
        attachment_1,
        patient_1,
        appointment_patient_1,
        upload_file,
        stored_file,
    ):
        attachment_service.uow.users.get_patient_by_id = AsyncMock(
            return_value=patient_1
        )

        attachment_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=appointment_patient_1
        )

        attachment_service.storage.save = AsyncMock(return_value=stored_file)

        attachment_service.uow.attachments.create_attachment = AsyncMock(
            return_value=attachment_1
        )

        result = await attachment_service.create(
            data=attachment_create_schema,
            file=upload_file,
            current_user=current_doctor,
        )

        attachment_service.uow.users.get_patient_by_id.assert_awaited_once_with(
            patient_id=attachment_create_schema.patient_id,
        )

        attachment_service.uow.appointments.get_appointment_by_id.assert_awaited_once_with(
            appointment_id=attachment_create_schema.appointment_id,
        )

        attachment_service.storage.save.assert_awaited_once_with(
            file=upload_file,
        )

        attachment_service.uow.attachments.create_attachment.assert_awaited_once()

        call = attachment_service.uow.attachments.create_attachment.await_args

        assert call.kwargs["uploaded_by_id"] == current_doctor.id

        data = call.kwargs["data"]

        assert isinstance(data, AttachmentSchema)
        assert data.filename == upload_file.filename
        assert data.file_path == stored_file.key
        assert data.file_size == stored_file.size
        assert data.file_mime_type == stored_file.content_type
        assert data.patient_id == patient_1.id
        assert data.appointment_id == appointment_patient_1.id

        assert isinstance(result, AttachmentResponseSchema)
        assert result.id == attachment_1.id

    @pytest.mark.asyncio
    async def test_create_attachment_not_user_found(
        self,
        attachment_service,
        current_doctor,
        attachment_create_schema,
        upload_file,
    ):
        attachment_service.uow.users.get_patient_by_id = AsyncMock(return_value=None)
        attachment_service.uow.appointments.get_appointment_by_id = AsyncMock()
        attachment_service.storage.save = AsyncMock()
        attachment_service.uow.attachments.create_attachment = AsyncMock()

        with pytest.raises(UserNotFoundException):
            await attachment_service.create(
                data=attachment_create_schema,
                file=upload_file,
                current_user=current_doctor,
            )

        attachment_service.uow.users.get_patient_by_id.assert_awaited_once_with(
            patient_id=attachment_create_schema.patient_id,
        )
        attachment_service.uow.appointments.get_appointment_by_id.assert_not_awaited()
        attachment_service.storage.save.assert_not_awaited()
        attachment_service.uow.attachments.create_attachment.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_attachment_not_appointment_found(
        self,
        attachment_service,
        current_doctor,
        attachment_create_schema,
        patient_1,
        upload_file,
    ):
        attachment_service.uow.users.get_patient_by_id = AsyncMock(
            return_value=patient_1
        )

        attachment_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=None
        )

        attachment_service.storage.save = AsyncMock()
        attachment_service.uow.attachments.create_attachment = AsyncMock()

        with pytest.raises(AppointmentNotFoundException):
            await attachment_service.create(
                data=attachment_create_schema,
                file=upload_file,
                current_user=current_doctor,
            )

        attachment_service.uow.users.get_patient_by_id.assert_awaited_once_with(
            patient_id=attachment_create_schema.patient_id,
        )

        attachment_service.uow.appointments.get_appointment_by_id.assert_awaited_once_with(
            appointment_id=attachment_create_schema.appointment_id,
        )

        attachment_service.storage.save.assert_not_awaited()
        attachment_service.uow.attachments.create_attachment.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_attachment_for_wrong_appointment_patient(
        self,
        attachment_service,
        current_doctor,
        attachment_create_schema,
        patient_1,
        appointment_patient_2,
        upload_file,
    ):
        attachment_service.uow.users.get_patient_by_id = AsyncMock(
            return_value=patient_1
        )

        attachment_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=appointment_patient_2
        )

        attachment_service.storage.save = AsyncMock()
        attachment_service.uow.attachments.create_attachment = AsyncMock()

        with pytest.raises(AppointmentRelatesToDifferentPatientException):
            await attachment_service.create(
                data=attachment_create_schema,
                file=upload_file,
                current_user=current_doctor,
            )

        attachment_service.uow.users.get_patient_by_id.assert_awaited_once_with(
            patient_id=attachment_create_schema.patient_id,
        )

        attachment_service.uow.appointments.get_appointment_by_id.assert_awaited_once_with(
            appointment_id=attachment_create_schema.appointment_id,
        )

        attachment_service.storage.save.assert_not_awaited()
        attachment_service.uow.attachments.create_attachment.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_attachment_success(
        self,
        attachment_service,
        current_doctor,
        attachment_update_schema,
        attachment_1,
        patient_1,
        appointment_patient_1,
        attachment_2,
    ):
        attachment_service.uow.attachments.get_attachment_by_id = AsyncMock(
            return_value=attachment_1
        )
        attachment_service.uow.attachments.update_attachment = AsyncMock(
            return_value=attachment_2
        )
        attachment_service.policy.can_update = MagicMock()
        result = await attachment_service.update(
            1,
            attachment_update_schema,
            current_doctor,
        )
        attachment_service.uow.attachments.get_attachment_by_id.assert_awaited_once_with(
            attachment_id=1,
        )
        attachment_service.uow.attachments.update_attachment.assert_awaited_once_with(
            attachment=attachment_1,
            data=attachment_update_schema,
        )
        attachment_service.policy.can_update.assert_called_once_with(
            user=current_doctor, attachment=attachment_1
        )
        assert isinstance(result, AttachmentResponseSchema)

    @pytest.mark.asyncio
    async def test_update_attachment_attachment_not_found(
        self,
        attachment_service,
        current_doctor,
        attachment_update_schema,
    ):
        attachment_service.uow.attachments.get_attachment_by_id = AsyncMock(
            return_value=None
        )

        with pytest.raises(AttachmentDoesNotExistException):
            await attachment_service.update(
                attachment_id=1,
                data=attachment_update_schema,
                current_user=current_doctor,
            )

        attachment_service.uow.attachments.get_attachment_by_id.assert_awaited_once_with(
            attachment_id=1,
        )

        attachment_service.uow.attachments.update_attachment.assert_not_called()
        attachment_service.policy.can_update.assert_not_called()

    @pytest.mark.asyncio
    async def test_delete_attachment_success(
        self,
        attachment_service,
        current_doctor,
        attachment_1,
    ):
        attachment_service.uow.attachments.get_attachment_by_id = AsyncMock(
            return_value=attachment_1
        )

        attachment_service.uow.attachments.delete_attachment = AsyncMock()

        attachment_service.storage.delete = AsyncMock()

        attachment_service.policy.can_delete = MagicMock()

        result = await attachment_service.delete(
            attachment_id=1,
            current_user=current_doctor,
        )

        attachment_service.uow.attachments.get_attachment_by_id.assert_awaited_once_with(
            attachment_id=1,
        )

        attachment_service.policy.can_delete.assert_called_once_with(
            user=current_doctor,
            attachment=attachment_1,
        )

        attachment_service.storage.delete.assert_awaited_once_with(
            attachment_1.file_path,
        )

        attachment_service.uow.attachments.delete_attachment.assert_awaited_once_with(
            attachment=attachment_1,
        )

        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self,
        attachment_service,
        attachment_1,
    ):
        attachment_service.uow.attachments.get_attachment_by_id = AsyncMock(
            return_value=attachment_1
        )
        result = await attachment_service.get_by_id(
            attachment_id=1,
        )
        attachment_service.uow.attachments.get_attachment_by_id.assert_awaited_once_with(
            attachment_id=1,
        )
        assert isinstance(result, AttachmentResponseSchema)
        assert result.id == attachment_1.id

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(
        self,
        attachment_service,
    ):
        attachment_service.uow.attachments.get_attachment_by_id = AsyncMock(
            return_value=None
        )

        with pytest.raises(AttachmentDoesNotExistException):
            await attachment_service.get_by_id(
                attachment_id=1,
            )

        attachment_service.uow.attachments.get_attachment_by_id.assert_awaited_once_with(
            attachment_id=1,
        )

    @pytest.mark.asyncio
    async def test_get_by_appointment_id_success(
        self,
        attachment_service,
        attachment_1,
        pagination,
    ):
        attachment_service.uow.attachments.get_attachments_by_appointment_id = (
            AsyncMock(
                return_value=PaginationResult(
                    items=[attachment_1],
                    total=1,
                )
            )
        )

        result = await attachment_service.get_by_appointment_id(
            appointment_id=1,
            pagination=pagination,
        )

        attachment_service.uow.attachments.get_attachments_by_appointment_id.assert_awaited_once_with(
            appointment_id=1,
            pagination=pagination,
        )

        assert result.total == 1
        assert result.page == 1
        assert result.page_size == 20
        assert result.pages == 1

        assert len(result.items) == 1
        assert isinstance(result.items[0], AttachmentResponseSchema)
        assert result.items[0].id == attachment_1.id

    @pytest.mark.asyncio
    async def test_get_by_appointment_id_not_found(
        self,
        attachment_service,
        pagination,
    ):
        attachment_service.uow.attachments.get_attachments_by_appointment_id = (
            AsyncMock(
                return_value=PaginationResult(
                    items=[],
                    total=0,
                )
            )
        )

        result = await attachment_service.get_by_appointment_id(
            appointment_id=1,
            pagination=pagination,
        )

        attachment_service.uow.attachments.get_attachments_by_appointment_id.assert_awaited_once_with(
            appointment_id=1,
            pagination=pagination,
        )

        assert result.total == 0
        assert result.page == 1
        assert result.page_size == 20
        assert result.pages == 0
        assert result.items == []

    @pytest.mark.asyncio
    async def test_get_by_patient_id_success(
        self,
        attachment_service,
        attachment_1,
        pagination,
    ):
        attachment_service.uow.attachments.get_attachments_by_patient_id = AsyncMock(
            return_value=PaginationResult(
                items=[attachment_1],
                total=1,
            )
        )

        result = await attachment_service.get_by_patient_id(
            patient_id=1,
            pagination=pagination,
        )

        attachment_service.uow.attachments.get_attachments_by_patient_id.assert_awaited_once_with(
            patient_id=1,
            pagination=pagination,
        )

        assert result.total == 1
        assert result.page == 1
        assert result.page_size == 20
        assert result.pages == 1

        assert len(result.items) == 1
        assert isinstance(result.items[0], AttachmentResponseSchema)
        assert result.items[0].id == attachment_1.id

    @pytest.mark.asyncio
    async def test_get_by_patient_id_not_found(
        self,
        attachment_service,
        pagination,
    ):
        attachment_service.uow.attachments.get_attachments_by_patient_id = AsyncMock(
            return_value=PaginationResult(
                items=[],
                total=0,
            )
        )

        result = await attachment_service.get_by_patient_id(
            patient_id=1,
            pagination=pagination,
        )

        attachment_service.uow.attachments.get_attachments_by_patient_id.assert_awaited_once_with(
            patient_id=1,
            pagination=pagination,
        )

        assert result.total == 0
        assert result.page == 1
        assert result.page_size == 20
        assert result.pages == 0  # или 1, если так реализован build_paginated_response
        assert result.items == []
