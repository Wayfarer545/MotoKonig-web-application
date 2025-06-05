import pytest

from app.domain.entities.user import User, UserRole


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

