import pytest

from app.application.use_cases.auth.logout import LogoutUseCase
from app.domain.ports.services.token import TokenServicePort


class DummyTokenService(TokenServicePort):
    def __init__(self):
        self.blacklisted = []
        self.tokens = {}

    async def create_access_token(self, data: dict, expires_delta: int | None = None) -> str:  # pragma: no cover
        raise NotImplementedError

    async def create_refresh_token(self, data: dict, expires_delta: int | None = None) -> str:  # pragma: no cover
        raise NotImplementedError

    async def decode_token(self, token: str) -> dict:
        if token == "bad":
            raise ValueError("bad token")
        return {"exp": 42}

    async def blacklist_token(self, token: str, expire_time: int) -> None:
        self.blacklisted.append((token, expire_time))

    async def is_token_blacklisted(self, token: str) -> bool:  # pragma: no cover
        return False


@pytest.mark.asyncio
async def test_logout_valid_token():
    svc = DummyTokenService()
    uc = LogoutUseCase(svc)
    await uc.execute("good")
    assert svc.blacklisted == [("good", 42)]


@pytest.mark.asyncio
async def test_logout_invalid_token():
    svc = DummyTokenService()
    uc = LogoutUseCase(svc)
    await uc.execute("bad")
    assert svc.blacklisted == []
