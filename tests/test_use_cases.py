import pytest
from redis.asyncio import Redis

from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.application.use_cases.auth.register import RegisterUseCase
from app.application.use_cases.user.update_user import UpdateUserUseCase
from app.adapters.specifications.user_specs.user_by_name import UserByName
from app.config.settings import SecuritySettings
from app.domain.entities.user import UserRole
from app.infrastructure.services.password_service import PasswordServiceImpl
from app.infrastructure.services.token_service import JWTTokenService
from tests.fake_repo import FakeUserRepository


@pytest.fixture
async def components():
    repo = FakeUserRepository()
    pwd = PasswordServiceImpl()
    redis = Redis()
    token_svc = JWTTokenService(redis, SecuritySettings())
    return repo, pwd, token_svc, redis


@pytest.mark.asyncio
async def test_register_and_login_flow(components):
    repo, pwd, token_svc, redis = components
    register_uc = RegisterUseCase(repo, pwd)
    login_uc = LoginUseCase(repo, pwd, token_svc)

    user = await register_uc.execute("admin", "pass")
    assert user.role == UserRole.ADMIN

    tokens = await login_uc.execute("admin", "pass")
    payload = await token_svc.decode_token(tokens["access_token"])
    assert payload["username"] == "admin"

    await redis.aclose()


@pytest.mark.asyncio
async def test_refresh_blacklists_old_token(components):
    repo, pwd, token_svc, redis = components
    register_uc = RegisterUseCase(repo, pwd)
    login_uc = LoginUseCase(repo, pwd, token_svc)
    refresh_uc = RefreshTokenUseCase(token_svc, repo)

    await register_uc.execute("user", "pass")
    tokens = await login_uc.execute("user", "pass")
    new_tokens = await refresh_uc.execute(tokens["refresh_token"])
    assert new_tokens["access_token"] != tokens["access_token"]

    with pytest.raises(ValueError):
        await refresh_uc.execute(tokens["refresh_token"])
    await redis.aclose()


@pytest.mark.asyncio
async def test_update_user(components):
    repo, pwd, token_svc, redis = components
    register_uc = RegisterUseCase(repo, pwd)
    user = await register_uc.execute("user2", "pass")

    update_uc = UpdateUserUseCase(repo, pwd)
    await update_uc.execute(user.id, new_username="newname", new_password="newpass")
    updated = await repo.get(UserByName("newname"))
    assert updated.username == "newname"
    assert await pwd.verify("newpass", updated.password_hash)
    await redis.aclose()
