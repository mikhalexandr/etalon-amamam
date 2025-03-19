import redis.asyncio as redis

from core.redis.initialization import RedisClient


async def get_redis() -> redis.Redis:
    return RedisClient.get_redis()
