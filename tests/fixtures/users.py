import pytest

from app.users.models.user import User
from common.enums.user_role import UserRole


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
def admin():
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