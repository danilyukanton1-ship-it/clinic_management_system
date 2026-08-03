from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.exceptions.token import InvalidTokenException
from app.auth.schemas.me import MeSchema
from app.auth.services.login import LoginService
from app.auth.services.register import RegisterService
from app.auth.services.token import TokenService
from app.users.exceptions.user import UserNotFoundException
from core.dependencies import get_redis, get_session, get_uow
from db.unit_of_work import UnitOfWork


async def get_login_service(
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
) -> LoginService:
    return LoginService(session=session, redis=redis)


async def get_register_service(
    session: AsyncSession = Depends(get_session),
    redis: Redis = Depends(get_redis),
):
    return RegisterService(session=session, redis=redis)


async def get_token_service(
    session: AsyncSession = Depends(get_session), redis: Redis = Depends(get_redis)
):
    return TokenService(session=session, redis=redis)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    uow: UnitOfWork = Depends(get_uow),
    token_service: TokenService = Depends(get_token_service),
) -> MeSchema:
    payload = token_service.decode_token(token)

    if payload["type"] != "access":
        raise InvalidTokenException()

    user_id = int(payload["sub"])

    user = await uow.users.get_user_by_id(user_id)

    if user is None:
        raise UserNotFoundException()

    return MeSchema.model_validate(user)
