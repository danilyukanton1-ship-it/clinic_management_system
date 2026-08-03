from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.services.specialization import SpecializationService
from app.users.services.user import UserService
from core.dependencies import get_redis, get_session


async def get_user_service(
    session: AsyncSession = Depends(get_session), redis: Redis = Depends(get_redis)
):
    return UserService(session=session, redis=redis)


async def get_specialization_service(session: AsyncSession = Depends(get_session)):
    return SpecializationService(session)
