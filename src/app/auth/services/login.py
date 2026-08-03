from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions.login import InvalidCredentialsException
from app.auth.exceptions.register import TooManyLoginAttemptsException
from app.auth.schemas.login import LoginSchema
from app.auth.schemas.token import TokenResponseSchema
from app.auth.security import verify_password
from app.auth.services.token import TokenService
from common.enums.token_type import TokenType
from db.unit_of_work import UnitOfWork


class LoginService:
    def __init__(self, session: AsyncSession, redis: Redis):
        self.uow = UnitOfWork(session)
        self.redis = redis

    async def login(self, data: LoginSchema) -> TokenResponseSchema:
        user = await self.uow.users.get_user_by_email(data.email)

        if not user or not user.is_active or not user.is_verified:
            raise InvalidCredentialsException()

        key = f"login_attempts:{user.email}"

        attempts = await self.redis.get(key)
        attempts = int(attempts) if attempts else 0

        if attempts >= 5:
            raise TooManyLoginAttemptsException()

        if not verify_password(data.password, user.password_hash):
            attempts = await self.redis.incr(key)
            if attempts == 1:
                await self.redis.expire(key, 900)
            raise InvalidCredentialsException()

        access_token = TokenService.create_token(
            user_id=user.id,
            email=user.email,
            role=user.role.value,
            token_type=TokenType.ACCESS,
        )

        refresh_token = TokenService.create_token(
            user_id=user.id,
            email=user.email,
            role=user.role.value,
            token_type=TokenType.REFRESH,
        )
        await self.redis.delete(key)
        return TokenResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
        )
