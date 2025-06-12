# tests/factories/user_factory.py
from uuid import uuid4

from app.domain.entities.user import User
from app.domain.value_objects.user_role import UserRole


class UserFactory:
    """Фабрика для создания пользователей в тестах"""

    @staticmethod
    def create(**kwargs) -> User:
        defaults = {
            "username": f"testuser_{uuid4().hex[:8]}",
            "password_hash": "hashed_password_123",
            "role": UserRole.USER,
        }
        defaults.update(kwargs)
        return User(**defaults)

    @staticmethod
    def create_admin(**kwargs) -> User:
        kwargs.setdefault("role", UserRole.ADMIN)
        kwargs.setdefault("username", f"admin_{uuid4().hex[:8]}")
        return UserFactory.create(**kwargs)

    @staticmethod
    def create_batch(count: int, **kwargs) -> list[User]:
        return [UserFactory.create(**kwargs) for _ in range(count)]

