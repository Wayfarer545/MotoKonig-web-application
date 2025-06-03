# app/infrastructure/adapters/redis/client.py

import redis.asyncio as redis
from app.config.settings import RedisConfig


async def create_redis_client(config: RedisConfig) -> redis.Redis:
    return redis.Redis(
        host=config.redis_host,
        port=config.redis_port,
        decode_responses=True
    )