from unittest.mock import MagicMock

import pytest

from app.medical_records.models.diagnosis import Diagnosis
from app.medical_records.models.disease import Disease
from app.medical_records.models.drug import Drug
from app.medical_records.models.prescription import Prescription
from app.medical_records.models.prescription_item import PrescriptionItem
from app.medical_records.schemas.diagnosis import DiagnosisCreateSchema, DiagnosisUpdateSchema
from app.medical_records.schemas.disease import DiseaseUpdateSchema, DiseaseCreateSchema
from app.medical_records.services.diagnosis import DiagnosisService
from app.medical_records.services.disease import DiseaseService
from common.enums.dosage_form import DosageForm

@pytest.fixture
def diagnosis_service(mock_async_session, mock_uow):
    service = DiagnosisService(mock_async_session)
    service.uow = mock_uow
    service.policy = MagicMock()
    return service

@pytest.fixture
def disease_service(mock_async_session, mock_uow):
    service = DiseaseService(mock_async_session)
    service.uow = mock_uow
    return service


@pytest.fixture
def diagnosis_create_schema():
    return DiagnosisCreateSchema(
        prescription_id=1,
        disease_id=1,
        notes="test notes",
    )

@pytest.fixture
def diagnosis_update_schema():
    return DiagnosisUpdateSchema(
        disease_id=2,
        notes="test notes 2",
    )

@pytest.fixture
def disease_update_schema():
    return DiseaseUpdateSchema(
        code="AA22",
        name="test name 2",
        description="test description 2",
    )

@pytest.fixture
def disease_create_schema():
    return DiseaseCreateSchema(
        code="FA21",
        name="test name",
        description="test description",
    )


@pytest.fixture
def disease_1():
    return Disease(
        id=1,
        code="FA21",
        description="test description",
        name="test name",
    )

@pytest.fixture
def disease_1_updated():
    return Disease(
        id=1,
        code="AA22",
        description="test description 2",
        name="test name 2"
    )


@pytest.fixture
def diagnosis():
    return Diagnosis(
        id=1,
        prescription_id=1,
        disease_id=1,
        notes="test notes",
    )

@pytest.fixture
def diagnosis_updated():
    return Diagnosis(
        id=1,
        prescription_id=1,
        disease_id=2,
        notes="test notes 2",
    )

@pytest.fixture
def prescription():
    return Prescription(
        id=1,
        appointment_id=1,
    )

@pytest.fixture
def drug():
    return Drug(
        id=1,
        name="test name",
        international_name="test international name",
        dosage_form=DosageForm.CAPSULE,
        strength='test strength',
        description='test description',
    )

@pytest.fixture
def prescription_item_1():
    return PrescriptionItem(
        id=1,
        prescription_id=1,
        drug_id=1,
        dosage='test dosage',
        frequency='test frequency',
        duration_days='test duration days',
    )

@pytest.fixture
def prescription_item_2():
    return PrescriptionItem(
        id=2,
        prescription_id=1,
        drug_id=1,
        dosage='test dosage 2',
        frequency='test frequency 2',
        duration_days='test duration days 2',
    )
