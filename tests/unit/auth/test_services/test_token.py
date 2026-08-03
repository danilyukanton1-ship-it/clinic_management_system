from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock

import jwt
import pytest

from app.auth.exceptions.token import (
    InvalidTokenException,
    InvalidTokenTypeException,
    TokenBlacklistedException,
    TokenExpiredException,
)
from app.auth.schemas.token import AccessTokenSchema
from app.users.exceptions.user import (
    UserInactiveException,
    UserNotFoundException,
)
from common.enums.token_type import TokenType
from core.config import settings


class TestTokenService:
    def test_create_access_token(
        self,
        patient_1,
        token_service,
    ):
        token = token_service.create_token(
            user_id=patient_1.id,
            email=patient_1.email,
            role=patient_1.role.value,
            token_type=TokenType.ACCESS,
        )

        payload = token_service.decode_token(token)

        assert payload["sub"] == str(patient_1.id)
        assert payload["type"] == TokenType.ACCESS.value
        assert payload["email"] == patient_1.email
        assert payload["role"] == patient_1.role.value
        assert "exp" in payload
        assert "jti" not in payload

    def test_create_refresh_token(
        self,
        patient_1,
        token_service,
    ):
        token = token_service.create_token(
            user_id=patient_1.id,
            email=patient_1.email,
            role=patient_1.role.value,
            token_type=TokenType.REFRESH,
        )

        payload = token_service.decode_token(token)

        assert payload["sub"] == str(patient_1.id)
        assert payload["type"] == TokenType.REFRESH.value
        assert "jti" in payload
        assert "email" not in payload
        assert "role" not in payload
        assert "exp" in payload

    def test_create_token_invalid_type(
        self,
        patient_1,
        token_service,
    ):
        with pytest.raises(InvalidTokenTypeException):
            token_service.create_token(
                user_id=patient_1.id,
                email=patient_1.email,
                role=patient_1.role.value,
                token_type="invalid",
            )

    def test_decode_token_success(
        self,
        patient_1,
        token_service,
    ):
        token = token_service.create_token(
            user_id=patient_1.id,
            email=patient_1.email,
            role=patient_1.role.value,
            token_type=TokenType.ACCESS,
        )

        payload = token_service.decode_token(token)

        assert payload["sub"] == str(patient_1.id)
        assert payload["type"] == TokenType.ACCESS.value
        assert payload["email"] == patient_1.email
        assert payload["role"] == patient_1.role.value

    def test_decode_token_expired(
        self,
        token_service,
    ):
        token = jwt.encode(
            {
                "sub": "1",
                "type": TokenType.ACCESS.value,
                "exp": datetime.now(UTC) - timedelta(minutes=1),
            },
            settings.jwt.SECRET_KEY,
            algorithm=settings.jwt.ALGORITHM,
        )

        with pytest.raises(TokenExpiredException):
            token_service.decode_token(token)

    def test_decode_token_invalid(
        self,
        token_service,
    ):
        with pytest.raises(InvalidTokenException):
            token_service.decode_token("invalid_token")

    @pytest.mark.asyncio
    async def test_get_access_token_success(
        self,
        token_service,
        patient_1,
    ):
        refresh_token = token_service.create_token(
            user_id=patient_1.id,
            email=patient_1.email,
            role=patient_1.role.value,
            token_type=TokenType.REFRESH,
        )

        token_service.is_blacklisted = AsyncMock(
            return_value=False,
        )

        token_service.uow.users.get_user_by_id = AsyncMock(
            return_value=patient_1,
        )

        result = await token_service.get_access_token(refresh_token)

        token_service.is_blacklisted.assert_called_once()

        token_service.uow.users.get_user_by_id.assert_called_once_with(
            patient_1.id,
        )

        assert isinstance(result, AccessTokenSchema)

        payload = token_service.decode_token(result.access_token)

        assert payload["sub"] == str(patient_1.id)
        assert payload["type"] == TokenType.ACCESS.value
        assert payload["email"] == patient_1.email
        assert payload["role"] == patient_1.role.value

    @pytest.mark.asyncio
    async def test_get_access_token_invalid_token_type(
        self,
        token_service,
        patient_1,
    ):
        access_token = token_service.create_token(
            user_id=patient_1.id,
            email=patient_1.email,
            role=patient_1.role.value,
            token_type=TokenType.ACCESS,
        )

        token_service.is_blacklisted = AsyncMock()

        token_service.uow.users.get_user_by_id = AsyncMock()

        with pytest.raises(InvalidTokenException):
            await token_service.get_access_token(access_token)

        token_service.is_blacklisted.assert_not_called()
        token_service.uow.users.get_user_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_access_token_blacklisted(
        self,
        token_service,
        patient_1,
    ):
        refresh_token = token_service.create_token(
            user_id=patient_1.id,
            email=patient_1.email,
            role=patient_1.role.value,
            token_type=TokenType.REFRESH,
        )

        token_service.is_blacklisted = AsyncMock(
            return_value=True,
        )

        token_service.uow.users.get_user_by_id = AsyncMock()

        with pytest.raises(TokenBlacklistedException):
            await token_service.get_access_token(refresh_token)

        token_service.is_blacklisted.assert_called_once()
        token_service.uow.users.get_user_by_id.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_access_token_user_not_found(
        self,
        token_service,
        patient_1,
    ):
        refresh_token = token_service.create_token(
            user_id=patient_1.id,
            email=patient_1.email,
            role=patient_1.role.value,
            token_type=TokenType.REFRESH,
        )

        token_service.is_blacklisted = AsyncMock(
            return_value=False,
        )

        token_service.uow.users.get_user_by_id = AsyncMock(
            return_value=None,
        )

        with pytest.raises(UserNotFoundException):
            await token_service.get_access_token(refresh_token)

        token_service.uow.users.get_user_by_id.assert_called_once_with(
            patient_1.id,
        )

    @pytest.mark.asyncio
    async def test_get_access_token_user_inactive(
        self,
        token_service,
        patient_1_inactive,
    ):
        refresh_token = token_service.create_token(
            user_id=patient_1_inactive.id,
            email=patient_1_inactive.email,
            role=patient_1_inactive.role.value,
            token_type=TokenType.REFRESH,
        )

        token_service.is_blacklisted = AsyncMock(
            return_value=False,
        )

        token_service.uow.users.get_user_by_id = AsyncMock(
            return_value=patient_1_inactive,
        )

        with pytest.raises(UserInactiveException):
            await token_service.get_access_token(refresh_token)

        token_service.uow.users.get_user_by_id.assert_called_once_with(
            patient_1_inactive.id,
        )

    @pytest.mark.asyncio
    async def test_blacklist_token_success(
        self,
        token_service,
        patient_1,
    ):
        refresh_token = token_service.create_token(
            user_id=patient_1.id,
            email=patient_1.email,
            role=patient_1.role.value,
            token_type=TokenType.REFRESH,
        )
        token_service.redis.set = AsyncMock()
        await token_service.blacklist_token(refresh_token)

        token_service.redis.set.assert_awaited_once()

        args, kwargs = token_service.redis.set.call_args

        assert args[0].startswith("blacklisted:")
        assert args[1] == "1"
        assert kwargs["ex"] > 0

    @pytest.mark.asyncio
    async def test_blacklist_token_expired(
        self,
        token_service,
    ):
        token = jwt.encode(
            {
                "sub": "1",
                "type": TokenType.REFRESH.value,
                "jti": "test-jti",
                "exp": int((datetime.now(UTC) - timedelta(minutes=1)).timestamp()),
            },
            settings.jwt.SECRET_KEY,
            algorithm=settings.jwt.ALGORITHM,
        )
        token_service.redis.set = AsyncMock()
        with pytest.raises(TokenExpiredException):
            await token_service.blacklist_token(token)

        token_service.redis.set.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_is_blacklisted_true(
        self,
        token_service,
    ):
        token_service.redis.exists = AsyncMock()
        token_service.redis.exists.return_value = 1
        result = await token_service.is_blacklisted("test-jti")

        token_service.redis.exists.assert_awaited_once_with(
            "blacklisted:test-jti",
        )

        assert result is True

    @pytest.mark.asyncio
    async def test_is_blacklisted_false(
        self,
        token_service,
    ):
        token_service.redis.exists = AsyncMock()
        token_service.redis.exists.return_value = 0

        result = await token_service.is_blacklisted("test-jti")

        token_service.redis.exists.assert_called_once_with(
            "blacklisted:test-jti",
        )

        assert result is False
