import pytest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession

from app.appointments.models.appointment import Appointment
from app.users.models.user import User
from common.enums.appointment_status import AppointmentStatus
from common.enums.user_role import UserRole

pytest_plugins = [
    "tests.fixtures.users",
    "tests.fixtures.appointments",
]

@pytest.fixture
def mock_async_session():
    return AsyncMock(spec=AsyncSession)

@pytest.fixture
def mock_uow():
    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=None)
    return uow

@pytest.fixture
def current_patient():
    return User(
        id=1,
        email="test@test.com",
        first_name="Test",
        last_name="Test",
        phone="+375290987654",
        role=UserRole.PATIENT,
        password_hash="ergerbgrengeur",
        is_verified=True,
        is_active=True,
    )

@pytest.fixture
def current_doctor():
    return User(
        id=1,
        email="test@test.com",
        first_name="Test",
        last_name="Test",
        phone="+375290987654",
        role=UserRole.DOCTOR,
        password_hash="ergerbgrengeur",
        specialization_id=1,
        is_verified=True,
        is_active=True,
    )

@pytest.fixture
def current_admin():
    return User(
        id=1,
        email="test@test.com",
        first_name="Test",
        last_name="Test",
        phone="+375290987654",
        role=UserRole.ADMIN,
        password_hash="ergerbgrengeur",
        is_verified=True,
        is_active=True,
    )

