import pytest
from unittest.mock import AsyncMock

from app.appointments.exceptions.appointment import AppointmentNotFoundException, \
    AppointmentRelatesToDifferentPatientException
from app.appointments.exceptions.attachment import AttachmentDoesNotExistException
from app.users.exceptions.user import UserNotFoundException
from tests.fixtures.appointments import attachment_service, attachment_2
from app.appointments.schemas.attachment import (
    AttachmentResponseSchema,
)

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
            ):
        attachment_service.uow.users.get_patient_by_id = AsyncMock(
            return_value=patient_1
        )

        attachment_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=appointment_patient_1
        )

        attachment_service.uow.attachments.create_attachment = AsyncMock(
            return_value=attachment_1
        )
        result = await attachment_service.create(
            attachment_create_schema,
            current_doctor,
        )
        attachment_service.uow.attachments.create_attachment.assert_awaited_once_with(
            data=attachment_create_schema,
            uploaded_by_id=current_doctor.id,
        )
        assert isinstance(result, AttachmentResponseSchema)

    @pytest.mark.asyncio
    async def test_create_attachment_not_user_found(
            self,
            attachment_service,
            current_doctor,
            attachment_create_schema,
            attachment_1,
            ):
        attachment_service.uow.users.get_patient_by_id = AsyncMock(return_value=None)
        with pytest.raises(UserNotFoundException):
            await attachment_service.create(
                attachment_create_schema,
                current_doctor,
            )
            attachment_service.uow.appointments.get_appointment_by_id.assert_not_awaited()
            attachment_service.uow.attachments.create_attachment.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_attachment_not_appointment_found(
            self,
            attachment_service,
            current_doctor,
            attachment_create_schema,
            attachment_1,
            patient_1,
            ):
        attachment_service.uow.users.get_patient_by_id = AsyncMock(
            return_value=patient_1
        )
        attachment_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(AppointmentNotFoundException):
            await attachment_service.create(
                attachment_create_schema,
                current_doctor,
            )
            attachment_service.uow.attachments.create_attachment.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_attachment_for_wrong_appointment_patient(
            self,
            attachment_service,
            current_doctor,
            attachment_create_schema,
            attachment_1,
            patient_1,
            appointment_patient_2
            ):
        attachment_service.uow.users.get_patient_by_id = AsyncMock(
            return_value=patient_1
        )
        attachment_service.uow.appointments.get_appointment_by_id = AsyncMock(
            return_value=appointment_patient_2
        )
        with pytest.raises(AppointmentRelatesToDifferentPatientException):
            await attachment_service.create(
                attachment_create_schema,
                current_doctor,
            )

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
        assert isinstance(result, AttachmentResponseSchema)

    @pytest.mark.asyncio
    async def test_update_attachment_attachment_not_found(
            self,
            attachment_service,
            current_doctor,
            attachment_update_schema,
            attachment_1,
            patient_1,
            appointment_patient_1,
    ):
        attachment_service.uow.attachments.get_attachment_by_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(AttachmentDoesNotExistException):
            await attachment_service.update(
                1,
                attachment_update_schema,
                current_doctor,
            )
            attachment_service.uow.attachments.get_attachment_by_id.assert_awaited_once_with(
                attachment_id=1,
            )
            attachment_service.uow.attachments.update_attachment.assert_not_awaited()

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
        attachment_service.uow.attachments.delete_attachment = AsyncMock(
            return_value=None
        )
        result = await attachment_service.delete(
            1,
            current_doctor
        )
        attachment_service.uow.attachments.get_attachment_by_id.assert_awaited_once_with(
            attachment_id=1,
        )
        attachment_service.uow.attachments.delete_attachment.assert_awaited_once_with(
            attachment=attachment_1,
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_attachment_not_found(
            self,
            attachment_service,
            current_doctor,
            attachment_1,
    ):
        attachment_service.uow.attachments.get_attachment_by_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(AttachmentDoesNotExistException):
            await attachment_service.delete(
                1,
                current_doctor
            )
            attachment_service.uow.attachments.delete_attachment.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_get_by_id_success(
        self,
        attachment_service,
        current_doctor,
        attachment_1,
    ):
        attachment_service.uow.attachments.get_attachment_by_id = AsyncMock(
            return_value=attachment_1
        )
        result = await attachment_service.get_by_id(
            1,
            current_doctor
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
        current_doctor,
    ):
        attachment_service.uow.attachments.get_attachment_by_id = AsyncMock(
            return_value=None
        )
        with pytest.raises(AttachmentDoesNotExistException):
            await attachment_service.get_by_id(
                1,
                current_doctor
            )

    @pytest.mark.asyncio
    async def test_get_by_appointment_id_success(
        self,
        attachment_service,
        current_doctor,
        attachment_1,
    ):
        attachment_service.uow.attachments.get_attachments_by_appointment_id = AsyncMock(
            return_value=[attachment_1]
        )
        result = await attachment_service.get_by_appointment_id(
            1,
            current_doctor
        )
        attachment_service.uow.attachments.get_attachments_by_appointment_id.assert_awaited_once_with(
            appointment_id=1
        )
        assert isinstance(result, list)
        assert isinstance(result[0], AttachmentResponseSchema)
        assert result[0].id == attachment_1.id

    @pytest.mark.asyncio
    async def test_get_by_appointment_id_not_found(
        self,
        attachment_service,
        current_doctor,
    ):
        attachment_service.uow.attachments.get_attachments_by_appointment_id = AsyncMock(
            return_value=[]
        )
        result = await attachment_service.get_by_appointment_id(
            1,
            current_doctor
        )
        assert isinstance(result, list)
        assert result == []

    @pytest.mark.asyncio
    async def test_get_by_patient_id_success(
        self,
        attachment_service,
        current_doctor,
        attachment_1,
    ):
        attachment_service.uow.attachments.get_attachments_by_patient_id = AsyncMock(
            return_value=[attachment_1]
        )
        result = await attachment_service.get_by_patient_id(
            1,
            current_doctor
        )
        attachment_service.uow.attachments.get_attachments_by_patient_id.assert_awaited_once_with(
            patient_id=1,
        )
        assert isinstance(result, list)
        assert isinstance(result[0], AttachmentResponseSchema)
        assert result[0].id == attachment_1.id

    @pytest.mark.asyncio
    async def test_get_by_patient_id_not_found(
        self,
        attachment_service,
        current_doctor,
    ):
        attachment_service.uow.attachments.get_attachments_by_patient_id = AsyncMock(
            return_value=[]
        )
        result = await attachment_service.get_by_patient_id(
            1,
            current_doctor
        )
        assert isinstance(result, list)
        assert result == []
