from datetime import timedelta
from uuid import uuid4

import fakeredis.aioredis as fakeredis
import pytest
from redis.asyncio import Redis

from app.infrastructure.services.pin_storage import RedisPinStorage


@pytest.mark.asyncio
async def test_pin_storage_basic_ops():
    redis: Redis = fakeredis.FakeRedis(decode_responses=True)
    storage = RedisPinStorage(redis)
    user_id = uuid4()
    device_id = "dev1"
    await storage.save_pin(user_id, device_id, "hash", "phone", "token", ttl=timedelta(seconds=1))
    data = await storage.get_pin_data(user_id, device_id)
    assert data["device_name"] == "phone"
    await storage.increment_failed_attempts(user_id, device_id)
    assert await storage.get_failed_attempts(user_id, device_id) == 1
    await storage.reset_failed_attempts(user_id, device_id)
    assert await storage.get_failed_attempts(user_id, device_id) == 0
    await storage.update_last_login(user_id, device_id, "now")
    devices = await storage.get_user_devices(user_id)
    assert devices[0]["device_id"] == device_id
    await storage.delete_pin(user_id, device_id)
    assert await storage.get_pin_data(user_id, device_id) is None
    await storage.add_device_to_blacklist(user_id, device_id, ttl=1)
    await redis.close()
