import redis.asyncio as redis

from core.logger import logger
from core.settings import settings


class RedisClient:
    _client: redis.Redis | None = None

    @classmethod
    async def init_redis(cls) -> None:
        if cls._client is not None:
            logger.error("Redis is already initialized")
            return None

        cls._client = redis.from_url(settings.get_redis_url())
        logger.info("Redis initialized")

    @classmethod
    async def close_redis(cls) -> None:
        if cls._client is not None:
            logger.info("Redis closed")
            await cls._client.close()
            cls._client = None

    @classmethod
    def get_redis(cls) -> redis.Redis:
        return cls._client
