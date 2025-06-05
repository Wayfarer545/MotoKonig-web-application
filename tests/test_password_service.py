import pytest

from app.infrastructure.services.password_service import PasswordServiceImpl


@pytest.mark.asyncio
async def test_password_hash_and_verify():
    svc = PasswordServiceImpl()
    hashed = await svc.hash("secret")
    assert await svc.verify("secret", hashed)
    assert not await svc.verify("wrong", hashed)
