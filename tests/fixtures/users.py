from unittest.mock import MagicMock

import pytest

from app.users.models.specialization import Specialization
from app.users.models.user import User
from app.users.schemas.specialization import SpecializationUpdateSchema, SpecializationCreateSchema
from app.users.schemas.user import DoctorCreateSchema, DoctorUpdateSchema, AdminCreateSchema, AdminUpdateSchema, \
    PatientUpdateSchema
from app.users.services.specialization import SpecializationService
from app.users.services.user import UserService
from common.enums.user_role import UserRole

@pytest.fixture
def user_service(mock_async_session, mock_uow) -> UserService:
    service = UserService(mock_async_session)
    service.uow = mock_uow
    service.policy = MagicMock()
    return service

@pytest.fixture
def specialization_service(mock_async_session, mock_uow) -> SpecializationService:
    service = SpecializationService(mock_async_session)
    service.uow = mock_uow
    return service

@pytest.fixture
def patient_1():
    return User(
        id=1,
        email="patient1@test.com",
        first_name="PatientOne",
        last_name="PatientOne",
        phone="+375291111111",
        role=UserRole.PATIENT,
        password_hash="ergerbgrengeur",
        is_verified=True,
        is_active=True,
    )

@pytest.fixture
def patient_2():
    return User(
        id=2,
        email="patient2@test.com",
        first_name="PatientTwo",
        last_name="PatientTwo",
        phone="+375292222222",
        role=UserRole.PATIENT,
        password_hash="ergerbgrengeur",
        is_verified=True,
        is_active=True,
    )

@pytest.fixture
def doctor_1():
    return User(
        id=1,
        email="test1@test.com",
        first_name="DoctorOne",
        last_name="DoctorOne",
        phone="+375299999999",
        role=UserRole.DOCTOR,
        specialization_id=1,
        password_hash="ergerbgrengeur",
        is_verified=True,
        is_active=True,
    )

@pytest.fixture
def doctor_2():
    return User(
        id=2,
        email="doctor2@test.com",
        first_name="DoctorTwo",
        last_name="DoctorTwo",
        phone="+375298888888",
        role=UserRole.DOCTOR,
        specialization_id=2,
        password_hash="ergerbgrengeur",
        is_verified=True,
        is_active=True,
    )

@pytest.fixture
def admin_1():
    return User(
        id=2,
        email="admin@test.com",
        first_name="Admin",
        last_name="Admin",
        phone="+375297777777",
        role=UserRole.ADMIN,
        password_hash="ergerbgrengeur",
        is_verified=True,
        is_active=True,
    )

@pytest.fixture
def admin_2():
    return User(
        id=2,
        email="admin2@test.com",
        first_name="AdminTwo",
        last_name="AdminTwo",
        phone="+375297777772",
        role=UserRole.ADMIN,
        password_hash="ergerbgrengeur",
        is_verified=True,
        is_active=True,
    )

@pytest.fixture
def specialization():
    return Specialization(
        id=1,
        name="test specialization",
        description="test specialization",
    )

@pytest.fixture
def specialization_update_schema():
    return SpecializationUpdateSchema(
        name="test specialization updated",
        description="test specialization updated",
    )

@pytest.fixture
def specialization_create_schema():
    return SpecializationCreateSchema(
        name="test specialization",
        description="test specialization",
    )

@pytest.fixture
def specialization_updated():
    return Specialization(
        id=1,
        name="test specialization updated",
        description="test specialization updated",
    )

@pytest.fixture
def doctor_create_schema():
    return DoctorCreateSchema(
        first_name = "test",
        last_name = "test",
        middle_name = "test",
        phone = "+375291234567",
        email = "doctor@test.com",
        password = "qwerty",
        specialization_id=1,
    )

@pytest.fixture
def admin_create_schema():
    return AdminCreateSchema(
        email="admin@test.com",
        first_name="Admin",
        middle_name="Admin",
        last_name="Admin",
        phone="+375297777777",
        password="qwerty",
    )

@pytest.fixture
def doctor_update_schema():
    return DoctorUpdateSchema(
        email="doctor2@test.com",
        first_name="DoctorTwo",
        last_name="DoctorTwo",
        phone="+375298888888",
        specialization_id=2,
    )

@pytest.fixture
def admin_update_schema():
    return AdminUpdateSchema(
        email="admin2@test.com",
        first_name="AdminTwo",
        last_name="AdminTwo",
        phone="+375297777772",
    )

@pytest.fixture
def patient_update_schema():
    return PatientUpdateSchema(
        email="patient2@test.com",
        first_name="PatientTwo",
        last_name="PatientTwo",
        phone="+375292222222",
    )

