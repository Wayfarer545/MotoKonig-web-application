import pytest
from fastapi import HTTPException, Request

from app.domain.entities.user import UserRole
from app.presentation.dependencies.auth import (
    check_role,
    get_current_user_dishka,
    get_token_from_header,
)


class DummyService:
    def __init__(self, payload: dict[str, str]):
        self.payload = payload
        self.blacklisted = set()

    async def decode_token(self, token: str) -> dict[str, str]:
        if token == "bad":
            raise ValueError("Invalid token")
        return self.payload

    async def is_token_blacklisted(self, token: str) -> bool:
        return token in self.blacklisted

    async def blacklist_token(self, token: str, expire: int) -> None:
        self.blacklisted.add(token)


@pytest.mark.asyncio
async def test_get_token_from_header():
    req = Request({'type': 'http', 'headers': [(b'authorization', b'Bearer t')], 'method': 'GET', 'path': '/'})
    assert await get_token_from_header(req) == 't'
    req = Request({'type': 'http', 'headers': [], 'method': 'GET', 'path': '/'})
    assert await get_token_from_header(req) is None
    req = Request({'type': 'http', 'headers': [(b'authorization', b'Basic t')], 'method': 'GET', 'path': '/'})
    assert await get_token_from_header(req) is None

@pytest.mark.asyncio
async def test_get_current_user():
    service = DummyService({'sub': '12345678-1234-5678-1234-567812345678', 'username': 'u', 'role': 'ADMIN', 'type': 'access'})
    req = Request({'type': 'http', 'headers': [(b'authorization', b'Bearer ok')], 'method': 'GET', 'path': '/'})
    user = await get_current_user_dishka(req, service)
    assert user['role'] == UserRole.ADMIN

    service.blacklisted.add('bad')
    req = Request({'type': 'http', 'headers': [(b'authorization', b'Bearer bad')], 'method': 'GET', 'path': '/'})
    with pytest.raises(HTTPException):
        await get_current_user_dishka(req, service)

@pytest.mark.asyncio
async def test_get_current_user_missing_token():
    service = DummyService({'sub': '1'*36, 'username': 'u', 'role': 'ADMIN', 'type': 'access'})
    req = Request({'type': 'http', 'headers': [], 'method': 'GET', 'path': '/'})
    with pytest.raises(HTTPException):
        await get_current_user_dishka(req, service)


@pytest.mark.asyncio
async def test_get_current_user_decode_error():
    service = DummyService({'sub': '1'*36, 'username': 'u', 'role': 'ADMIN', 'type': 'access'})
    req = Request({'type': 'http', 'headers': [(b'authorization', b'Bearer bad')], 'method': 'GET', 'path': '/'})
    with pytest.raises(HTTPException):
        await get_current_user_dishka(req, service)


@pytest.mark.asyncio
async def test_get_current_user_invalid_type():
    service = DummyService({'sub': '1'*36, 'username': 'u', 'role': 'ADMIN', 'type': 'refresh'})
    req = Request({'type': 'http', 'headers': [(b'authorization', b'Bearer ok')], 'method': 'GET', 'path': '/'})
    with pytest.raises(HTTPException):
        await get_current_user_dishka(req, service)


def test_check_role():
    user = {'role': UserRole.ADMIN}
    check_role(user, [UserRole.ADMIN])
    with pytest.raises(HTTPException):
        check_role(user, [UserRole.USER])
