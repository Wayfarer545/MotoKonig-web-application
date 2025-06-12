import pytest

from app.domain.entities.user import User
from app.domain.value_objects.user_role import UserRole


def test_user_creation_and_dto():
    user = User(username="Admin", password_hash="hash", role=UserRole.ADMIN)
    dto = user.to_dto()
    assert dto["username"] == "admin"
    assert dto["role"] == UserRole.ADMIN
    assert dto["is_active"] is True


def test_user_change_username_and_deactivate():
    user = User(username="test", password_hash="hash")
    user.change_username("NewName")
    assert user.username == "newname"
    user.deactivate()
    assert not user.is_active


@pytest.mark.parametrize("name", ["", "ab"])
def test_invalid_username(name):
    with pytest.raises(ValueError):
        User(username=name, password_hash="h")


def test_password_required():
    with pytest.raises(ValueError):
        User(username="valid", password_hash="")


def test_change_username_invalid():
    user = User(username="valid", password_hash="hash")
    with pytest.raises(ValueError):
        user.change_username("ab")
