import pytest
from unittest.mock import AsyncMock, patch

from app.auth.exceptions.login import InvalidCredentialsException
from app.auth.exceptions.register import TooManyLoginAttemptsException
from app.auth.schemas.token import TokenResponseSchema
from common.enums.token_type import TokenType

class TestLoginService:

    @pytest.mark.asyncio
    async def test_login_success(
            self,
            login_service,
            login_schema,
            patient_1,
    ):
        login_service.uow.users.get_user_by_email = AsyncMock(
            return_value=patient_1
        )

        login_service.redis.get.return_value = None
        login_service.redis.delete = AsyncMock()

        with (
            patch(
                "app.auth.services.login.verify_password",
                return_value=True,
            ),
            patch(
                "app.auth.services.login.TokenService.create_token"
            ) as mock_create_token,
        ):
            mock_create_token.side_effect = [
                "access_token",
                "refresh_token",
            ]

            result = await login_service.login(login_schema)

        login_service.uow.users.get_user_by_email.assert_called_once_with(
            login_schema.email
        )

        login_service.redis.get.assert_called_once_with(
            f"login_attempts:{patient_1.email}"
        )

        assert mock_create_token.call_count == 2

        mock_create_token.assert_any_call(
            user_id=patient_1.id,
            email=patient_1.email,
            role=patient_1.role.value,
            token_type=TokenType.ACCESS,
        )

        mock_create_token.assert_any_call(
            user_id=patient_1.id,
            email=patient_1.email,
            role=patient_1.role.value,
            token_type=TokenType.REFRESH,
        )

        login_service.redis.delete.assert_called_once_with(
            f"login_attempts:{patient_1.email}"
        )

        assert isinstance(result, TokenResponseSchema)
        assert result.access_token == "access_token"
        assert result.refresh_token == "refresh_token"

    import pytest


    @pytest.mark.asyncio
    async def test_login_user_not_found(
            self,
            login_service,
            login_schema,
    ):
        login_service.uow.users.get_user_by_email = AsyncMock(
            return_value=None
        )

        with pytest.raises(InvalidCredentialsException):
            await login_service.login(login_schema)

        login_service.uow.users.get_user_by_email.assert_called_once_with(
            login_schema.email
        )

        login_service.redis.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_inactive_user(
            self,
            login_service,
            login_schema,
            patient_1,
    ):
        patient_1.is_active = False

        login_service.uow.users.get_user_by_email = AsyncMock(
            return_value=patient_1
        )

        with pytest.raises(InvalidCredentialsException):
            await login_service.login(login_schema)

        login_service.redis.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_unverified_user(
            self,
            login_service,
            login_schema,
            patient_1,
    ):
        patient_1.is_verified = False

        login_service.uow.users.get_user_by_email = AsyncMock(
            return_value=patient_1
        )

        with pytest.raises(InvalidCredentialsException):
            await login_service.login(login_schema)

        login_service.redis.get.assert_not_called()


    @pytest.mark.asyncio
    async def test_login_too_many_attempts(
            self,
            login_service,
            login_schema,
            patient_1,
    ):
        login_service.uow.users.get_user_by_email = AsyncMock(
            return_value=patient_1
        )

        login_service.redis.get.return_value = "5"

        with pytest.raises(TooManyLoginAttemptsException):
            await login_service.login(login_schema)

        login_service.redis.get.assert_called_once_with(
            f"login_attempts:{patient_1.email}"
        )

        login_service.redis.incr.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_invalid_password_first_attempt(
            self,
            login_service,
            login_schema,
            patient_1,
    ):
        login_service.uow.users.get_user_by_email = AsyncMock(
            return_value=patient_1
        )

        login_service.redis.get.return_value = None
        login_service.redis.incr.return_value = 1

        with patch(
                "app.auth.services.login.verify_password",
                return_value=False,
        ):
            with pytest.raises(InvalidCredentialsException):
                await login_service.login(login_schema)

        key = f"login_attempts:{patient_1.email}"

        login_service.redis.incr.assert_called_once_with(key)
        login_service.redis.expire.assert_called_once_with(key, 900)

    @pytest.mark.asyncio
    async def test_login_invalid_password_not_first_attempt(
            self,
            login_service,
            login_schema,
            patient_1,
    ):
        login_service.uow.users.get_user_by_email = AsyncMock(
            return_value=patient_1
        )

        login_service.redis.get.return_value = "2"
        login_service.redis.incr.return_value = 3

        with patch(
                "app.auth.services.login.verify_password",
                return_value=False,
        ):
            with pytest.raises(InvalidCredentialsException):
                await login_service.login(login_schema)

        key = f"login_attempts:{patient_1.email}"

        login_service.redis.incr.assert_called_once_with(key)
        login_service.redis.expire.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_verify_password_called(
            self,
            login_service,
            login_schema,
            patient_1,
    ):
        login_service.uow.users.get_user_by_email = AsyncMock(
            return_value=patient_1
        )

        login_service.redis.get.return_value = None

        with (
            patch(
                "app.auth.services.login.verify_password",
                return_value=True,
            ) as mock_verify,
            patch(
                "app.auth.services.login.TokenService.create_token",
                side_effect=["access_token", "refresh_token"],
            ),
        ):
            await login_service.login(login_schema)

        mock_verify.assert_called_once_with(
            login_schema.password,
            patient_1.password_hash,
        )

    @pytest.mark.asyncio
    async def test_login_create_token_not_called_when_password_invalid(
            self,
            login_service,
            login_schema,
            patient_1,
    ):
        login_service.uow.users.get_user_by_email = AsyncMock(
            return_value=patient_1
        )

        login_service.redis.get.return_value = None
        login_service.redis.incr.return_value = 1

        with (
            patch(
                "app.auth.services.login.verify_password",
                return_value=False,
            ),
            patch(
                "app.auth.services.login.TokenService.create_token",
            ) as mock_create_token,
        ):
            with pytest.raises(InvalidCredentialsException):
                await login_service.login(login_schema)

        mock_create_token.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_verify_password_not_called_when_too_many_attempts(
            self,
            login_service,
            login_schema,
            patient_1,
    ):
        login_service.uow.users.get_user_by_email = AsyncMock(
            return_value=patient_1
        )

        login_service.redis.get.return_value = "5"

        with patch(
                "app.auth.services.login.verify_password",
        ) as mock_verify:
            with pytest.raises(TooManyLoginAttemptsException):
                await login_service.login(login_schema)

        mock_verify.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_delete_attempts_not_called_when_password_invalid(
            self,
            login_service,
            login_schema,
            patient_1,
    ):
        login_service.uow.users.get_user_by_email = AsyncMock(
            return_value=patient_1
        )

        login_service.redis.get.return_value = None
        login_service.redis.incr.return_value = 1

        with patch(
                "app.auth.services.login.verify_password",
                return_value=False,
        ):
            with pytest.raises(InvalidCredentialsException):
                await login_service.login(login_schema)

        login_service.redis.delete.assert_not_called()

    @pytest.mark.asyncio
    async def test_login_delete_attempts_not_called_when_too_many_attempts(
            self,
            login_service,
            login_schema,
            patient_1,
    ):
        login_service.uow.users.get_user_by_email = AsyncMock(
            return_value=patient_1
        )

        login_service.redis.get.return_value = "5"

        with pytest.raises(TooManyLoginAttemptsException):
            await login_service.login(login_schema)

        login_service.redis.delete.assert_not_called()

