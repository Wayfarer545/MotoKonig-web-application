import pytest
from redis.asyncio import Redis

from app.config.settings import RedisConfig
from app.infrastructure.messaging.redis_client import RedisClient


@pytest.mark.asyncio
async def test_client_pool_cycle(monkeypatch):
    await RedisClient.create_pool(RedisConfig())
    client = await RedisClient.get_client()
    assert isinstance(client, Redis)
    await RedisClient.close_pool()
    with pytest.raises(RuntimeError):
        await RedisClient.get_client()


