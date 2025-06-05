import fakeredis.aioredis as fakeredis
import pytest
from redis.asyncio import Redis

from app.config.settings import SecuritySettings
from app.infrastructure.services.token_service import JWTTokenService


@pytest.mark.asyncio
async def test_token_creation_and_blacklist():
    redis: Redis = fakeredis.FakeRedis(decode_responses=True)
    svc = JWTTokenService(redis, SecuritySettings())
    data = {"sub": "1", "username": "u", "role": "USER", "jti": "1"}
    token = await svc.create_access_token(data)
    payload = await svc.decode_token(token)
    assert payload["sub"] == "1"
    await svc.blacklist_token(token, payload["exp"])
    assert await svc.is_token_blacklisted(token)
    await redis.aclose()
