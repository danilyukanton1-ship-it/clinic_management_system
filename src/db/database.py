from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import DeclarativeBase
from core.config import settings

engine = create_async_engine(
    settings.db.async_db_url,
    echo=True,
    # Celery by using asyncio.run() creates new event loop for each task
    # NullPool to avoid asyncpg connection's trying to use different event loop
    poolclass=NullPool,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass
