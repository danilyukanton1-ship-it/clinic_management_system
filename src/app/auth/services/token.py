import jwt
from uuid import uuid4
from datetime import datetime, timedelta, UTC
from typing import Literal

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions.token import (
    InvalidTokenTypeException,
    InvalidTokenException,
    TokenExpiredException, TokenBlacklistedException,
)
from app.auth.schemas.token import AccessTokenSchema
from app.users.exceptions.user import UserNotFoundException, UserInactiveException
from core.config import settings
from db.unit_of_work import UnitOfWork

cache = Redis(host=settings.redis.HOST, port=settings.redis.PORT, db=0, decode_responses=True)


class TokenService:

    def __init__(self, session: AsyncSession):
        self.session = session

        self.uow = UnitOfWork(session)

    @staticmethod
    def create_token(
            user_id: int,
            email: str,
            role: str,
            token_type: Literal["access", "refresh"] = 'access',
    ) -> str:
        if token_type == 'access':
            expire = datetime.now(UTC) + timedelta(
                minutes=settings.jwt.ACCESS_TOKEN_EXPIRE_MINUTES
            )
            payload = {
                'sub': str(user_id),
                'role': role,
                'email': email,
                'type': 'access',
                'exp': expire,
            }
        elif token_type == 'refresh':
            expire = datetime.now(UTC) + timedelta(
                minutes=settings.jwt.REFRESH_TOKEN_EXPIRE_MINUTES
            )
            payload = {
                'sub': str(user_id),
                'jti': str(uuid4()),
                'type': 'refresh',
                'exp': expire,
            }
        else:
            raise InvalidTokenTypeException()

        return jwt.encode(
            payload,
            settings.jwt.SECRET_KEY,
            algorithm=settings.jwt.ALGORITHM
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, settings.jwt.SECRET_KEY, algorithms=[settings.jwt.ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
        except jwt.InvalidTokenError:
            raise InvalidTokenException()

    async def get_access_token(self, refresh_token: str) -> AccessTokenSchema:
        payload = self.decode_token(refresh_token)

        if payload['type'] != 'refresh':
            raise InvalidTokenException()

        jti = payload['jti']
        if await self.is_blacklisted(jti):
            raise TokenBlacklistedException()

        user_id = int(payload['sub'])


        user = await self.uow.users.get_user_by_id(user_id)

        if user is None:
            raise UserNotFoundException()

        if not user.is_active:
            raise UserInactiveException()

        access_token = self.create_token(
            user_id=user.id,
            email=user.email,
            role=user.role.value,
            token_type='access',
        )

        return AccessTokenSchema(access_token=access_token)

    async def blacklist_token(
            self,
            refresh_token: str,
    ) -> None:
        decoded_token = self.decode_token(refresh_token)
        jti = decoded_token['jti']
        exp = decoded_token['exp']
        ttl = exp - int(datetime.now(UTC).timestamp())
        if ttl <= 0:
            raise TokenExpiredException()
        await cache.set(
            f'blacklisted:{jti}',
            '1',
            ex=ttl,
        )

    @staticmethod
    async def is_blacklisted(
            jti: str,
    ) -> bool:
        return bool(await cache.exists(f'blacklisted:{jti}'))