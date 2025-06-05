import pytest
from fastapi import HTTPException

from app.application.controllers.auth_controller import AuthController
from app.domain.entities.user import UserRole


class DummyLogin:
    async def execute(self, u, p):
        if p == 'ok':
            return {'token': 't'}
        raise ValueError('bad')


class DummyLogout:
    async def execute(self, token):
        self.token = token


class DummyRefresh:
    async def execute(self, rt):
        if rt == 'r':
            return {'token': 'new'}
        raise ValueError('bad')


class DummyRegister:
    async def execute(self, u, p):
        if u == 'new':
            class User:
                id = '1'
                username = u
                role = UserRole.ADMIN
            return User()
        raise ValueError('exists')


class DummyPin:
    async def list_devices(self, user_id):
        return [{'id': 'd'}]

    async def revoke_device(self, user_id, dev):
        self.revoked = dev


controller = AuthController(DummyLogin(), DummyLogout(), DummyRefresh(), DummyRegister(), DummyPin())


@pytest.mark.asyncio
async def test_login_ok_and_fail():
    assert await controller.login('u', 'ok') == {'token': 't'}
    with pytest.raises(HTTPException):
        await controller.login('u', 'bad')


@pytest.mark.asyncio
async def test_refresh_and_register():
    assert await controller.refresh('r') == {'token': 'new'}
    with pytest.raises(HTTPException):
        await controller.refresh('bad')
    resp = await controller.register('new', 'p')
    assert resp['username'] == 'new'
    with pytest.raises(HTTPException):
        await controller.register('old', 'p')


@pytest.mark.asyncio
async def test_device_ops():
    devices = await controller.list_devices('1')
    assert devices[0]['id'] == 'd'
    await controller.revoke_device('1', 'd1')
    assert controller.pin_auth_uc.revoked == 'd1'
