from redis.asyncio import Redis

from core.config import settings

redis_client = Redis(
    host=settings.redis.HOST,
    port=settings.redis.PORT,
    db=0,
    decode_responses=True,
)
