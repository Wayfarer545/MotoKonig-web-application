from uuid import uuid4

import pytest

from app.application.controllers.user_controller import UserController
from app.application.exceptions import NotFoundError
from app.domain.entities.user import User, UserRole


class DummyUC:
    def __init__(self, result=None):
        self.result = result
        self.args = None

    async def execute(self, *args, **kwargs):
        self.args = (args, kwargs)
        return self.result


@pytest.mark.asyncio
async def test_user_controller_crud():
    list_uc = DummyUC([User(username='user', password_hash='h')])
    get_uc = DummyUC(User(username='user', password_hash='h'))
    create_uc = DummyUC(User(username='created', password_hash='h'))
    update_uc = DummyUC(User(username='user', password_hash='h'))
    delete_uc = DummyUC(True)

    ctrl = UserController(list_uc, get_uc, create_uc, update_uc, delete_uc)

    users = await ctrl.list_users()
    assert len(users) == 1
    user = await ctrl.get_user_by_id(uuid4())
    assert user['username'] == 'user'
    created = await ctrl.create('xxx', 'pwd', UserRole.USER)
    assert created.username == 'created'
    updated = await ctrl.update_user(uuid4(), 'u2', None, None)
    assert isinstance(updated, User)
    await ctrl.delete_user(uuid4())
    assert delete_uc.args[0][0] is not None


@pytest.mark.asyncio
async def test_update_delete_not_found():
    update_uc = DummyUC(None)
    ctrl = UserController(None, None, None, update_uc, DummyUC(False))
    with pytest.raises(NotFoundError):
        await ctrl.update_user(uuid4(), None, None, None)
    with pytest.raises(NotFoundError):
        await ctrl.delete_user(uuid4())

