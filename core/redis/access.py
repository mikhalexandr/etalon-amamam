import redis.asyncio as redis

from core.redis.initialization import RedisClient


# Получение клиента Redis
async def get_redis() -> redis.Redis:
    return RedisClient.get_redis()
