from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions.token import (
    InvalidTokenException,
    InvalidTokenTypeException,
    TokenBlacklistedException,
    TokenExpiredException,
)
from app.auth.schemas.token import AccessTokenSchema
from app.users.exceptions.user import UserInactiveException, UserNotFoundException
from common.enums.token_type import TokenType
from core.config import settings
from db.unit_of_work import UnitOfWork


class TokenService:

    def __init__(self, session: AsyncSession, redis: Redis) -> None:
        self.uow = UnitOfWork(session)
        self.redis = redis

    @staticmethod
    def create_token(
        user_id: int,
        email: str,
        role: str,
        token_type: TokenType,
    ) -> str:

        if token_type == TokenType.ACCESS:
            expire = datetime.now(UTC) + timedelta(
                minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        elif token_type == TokenType.REFRESH:
            expire = datetime.now(UTC) + timedelta(
                minutes=settings.jwt.REFRESH_TOKEN_EXPIRE_MINUTES
            )
        else:
            raise InvalidTokenTypeException()

        payload = {
            "sub": str(user_id),
            "type": token_type.value,
            "exp": expire,
        }

        if token_type == TokenType.ACCESS:
            payload.update(
                {
                    "email": email,
                    "role": role,
                }
            )

        elif token_type == TokenType.REFRESH:
            payload["jti"] = str(uuid4())

        return jwt.encode(
            payload,
            settings.jwt.SECRET_KEY,
            algorithm=settings.jwt.ALGORITHM,
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(
                token, settings.jwt.SECRET_KEY, algorithms=[settings.jwt.ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
        except jwt.InvalidTokenError:
            raise InvalidTokenException()

    async def get_access_token(self, refresh_token: str) -> AccessTokenSchema:
        payload = self.decode_token(refresh_token)

        if payload["type"] != TokenType.REFRESH.value:
            raise InvalidTokenException()

        jti = payload["jti"]
        if await self.is_blacklisted(jti):
            raise TokenBlacklistedException()

        user_id = int(payload["sub"])

        user = await self.uow.users.get_user_by_id(user_id)

        if user is None:
            raise UserNotFoundException()

        if not user.is_active:
            raise UserInactiveException()

        access_token = self.create_token(
            user_id=user.id,
            email=user.email,
            role=user.role.value,
            token_type=TokenType.ACCESS,
        )

        return AccessTokenSchema(access_token=access_token)

    async def blacklist_token(
        self,
        refresh_token: str,
    ) -> None:
        decoded_token = self.decode_token(refresh_token)
        jti = decoded_token["jti"]
        exp = decoded_token["exp"]
        ttl = exp - int(datetime.now(UTC).timestamp())
        if ttl <= 0:
            raise TokenExpiredException()
        await self.redis.set(
            f"blacklisted:{jti}",
            "1",
            ex=ttl,
        )

    async def is_blacklisted(
        self,
        jti: str,
    ) -> bool:
        return bool(await self.redis.exists(f"blacklisted:{jti}"))
