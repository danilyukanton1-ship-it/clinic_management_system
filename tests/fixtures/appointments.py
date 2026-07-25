from datetime import datetime

import pytest

from unittest.mock import MagicMock

from app.appointments.models.attachment import Attachment
from app.appointments.models.appointment import Appointment
from app.appointments.schemas.appointment import AppointmentCreateSchema
from app.appointments.services.attachment import AttachmentService
from app.appointments.services.appointment import AppointmentService
from common.enums.appointment_status import AppointmentStatus
from app.appointments.schemas.attachment import (
    AttachmentCreateSchema,
    AttachmentResponseSchema,
    AttachmentUpdateSchema
)

@pytest.fixture
def attachment_service(mock_async_session, mock_uow) -> AttachmentService:
    service = AttachmentService(mock_async_session)
    service.uow = mock_uow
    service.policy = MagicMock()
    return service

@pytest.fixture
def appointment_service(mock_async_session, mock_uow) -> AppointmentService:
    service = AppointmentService(mock_async_session)
    service.uow = mock_uow
    service.policy = MagicMock()
    return service

@pytest.fixture
def appointment_create_schema():
    return AppointmentCreateSchema(
        patient_id=1,
        doctor_id=1,
        slot_id=1,
    )


@pytest.fixture
def attachment_create_schema():
    return AttachmentCreateSchema(
        filename="test.pdf",
        file_path="/uploads/test.pdf",
        file_size=1024,
        file_mime_type="application/pdf",
        patient_id=1,
        appointment_id=1,
    )

@pytest.fixture
def attachment_update_schema():
    return AttachmentUpdateSchema(
        filename="test.jpg",
        file_path="/test/test.jpg",
        file_size=2048,
        file_mime_type="image/jpeg",
    )


@pytest.fixture
def attachment_response_schema_1():
    return AttachmentResponseSchema(
        id=1,
        filename="test.pdf",
        file_path="/uploads/test.pdf",
        file_size=1024,
        file_mime_type="application/pdf",
        patient_id=1,
        appointment_id=1,
        uploaded_by_id=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

@pytest.fixture
def attachment_response_schema_2():
    return AttachmentResponseSchema(
        id=1,
        filename="test.jpg",
        file_path="/test/test.jpg",
        file_size=2048,
        file_mime_type="image/jpeg",
        patient_id=1,
        appointment_id=1,
        uploaded_by_id=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

@pytest.fixture
def attachment_1():
    return Attachment(
        id=1,
        filename="test.pdf",
        file_path="/uploads/test.pdf",
        file_size=1024,
        file_mime_type="application/pdf",
        patient_id=1,
        appointment_id=1,
        uploaded_by_id=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

@pytest.fixture
def attachment_2():
    return Attachment(
        id=1,
        filename="test.jpg",
        file_path="/test/test.jpg",
        file_size=2048,
        file_mime_type="image/jpeg",
        patient_id=1,
        appointment_id=1,
        uploaded_by_id=10,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

@pytest.fixture
def appointment_patient_1(patient_1, doctor_1, schedule_slot_1, specialization):
    doctor_1.specialization = specialization

    appointment = Appointment(
        id=1,
        patient_id=patient_1.id,
        doctor_id=doctor_1.id,
        slot_id=schedule_slot_1.id,
        status=AppointmentStatus.SCHEDULED,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    appointment.patient = patient_1
    appointment.doctor = doctor_1
    appointment.slot = schedule_slot_1

    return appointment

@pytest.fixture
def appointment_patient_2():
    return Appointment(
        id=1,
        patient_id=2,
        doctor_id=1,
        slot_id=1,
        status=AppointmentStatus.SCHEDULED,
    )
