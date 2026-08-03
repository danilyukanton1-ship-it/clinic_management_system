import pytest

from app.auth.schemas.login import LoginSchema
from app.auth.schemas.register import (
    ForgotPasswordSchema,
    RegisterSchema,
    ResetPasswordSchema,
    VerifyEmailSchema,
)
from app.auth.services.login import LoginService
from app.auth.services.register import RegisterService
from app.auth.services.token import TokenService


@pytest.fixture
def login_service(mock_async_session, mock_redis) -> LoginService:
    service = LoginService(mock_async_session, mock_redis)
    return service


@pytest.fixture
def register_service(mock_async_session, mock_redis) -> RegisterService:
    service = RegisterService(mock_async_session, mock_redis)
    return service


@pytest.fixture
def token_service(mock_async_session, mock_redis) -> TokenService:
    service = TokenService(mock_async_session, mock_redis)
    return service


@pytest.fixture
def login_schema():
    return LoginSchema(
        email="patient@example.com",
        password="password123",
    )


@pytest.fixture
def register_schema():
    return RegisterSchema(
        first_name="patient",
        last_name="patient",
        middle_name="patient",
        email="patient@test.com",
        phone="+375291234567",
        password="password123",
    )


@pytest.fixture
def verify_email_schema():
    return VerifyEmailSchema(
        email="patient@test.com",
        verification_code="123456",
    )


@pytest.fixture
def forgot_password_schema():
    return ForgotPasswordSchema(
        email="patient@test.com",
    )


@pytest.fixture
def reset_password_schema():
    return ResetPasswordSchema(
        email="patient@test.com",
        verification_code="123456",
        password="password123",
    )
