import pytest
from unittest.mock import MagicMock, AsyncMock

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models.user import User
from common.enums.user_role import UserRole
from common.pagination.schemas import PaginationParams
from db.unit_of_work import UnitOfWork

pytest_plugins = [
    "tests.fixtures.users",
    "tests.fixtures.appointments",
    "tests.fixtures.scheduling",
    "tests.fixtures.medical_records",
    "tests.fixtures.auth",
]

@pytest.fixture
def pagination():
    return PaginationParams(
        page=1,
        page_size=20,
    )

@pytest.fixture
def mock_async_session() -> AsyncSession:
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def mock_storage() -> AsyncMock:
    storage = AsyncMock()
    return storage


@pytest.fixture
def mock_uow() -> UnitOfWork:
    uow = MagicMock()
    uow.__aenter__ = AsyncMock(return_value=uow)
    uow.__aexit__ = AsyncMock(return_value=None)
    return uow


@pytest.fixture
def mock_redis() -> Redis:
    redis = AsyncMock()

    redis.get = AsyncMock()
    redis.incr = AsyncMock()
    redis.expire = AsyncMock()
    redis.delete = AsyncMock()

    return redis


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
