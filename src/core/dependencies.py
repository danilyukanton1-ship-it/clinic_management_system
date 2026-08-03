from collections.abc import AsyncGenerator

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import AsyncSessionLocal
from db.redis import redis_client
from db.unit_of_work import UnitOfWork


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_uow(
    session: AsyncSession = Depends(get_session),
):
    return UnitOfWork(session)


async def get_redis() -> Redis:
    return redis_client
