# app/domain/entities/user.py

from __future__ import annotations
from uuid import UUID, uuid4
from enum import Enum
import datetime as dt

class UserRole(Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    USER = "user"

class User:
    """
    Сущность User. Инварианты проверяются в конструкторе,
    бизнес-логика (например, смена имени) инкапсулирована в методах.
    """
    def __init__(
        self,
        username: str,
        password_hash: str,
        role: UserRole = UserRole.USER,
        *,
        user_id: UUID | None = None,
        is_active: bool = True,
        created_at: dt | None = None,
        updated_at: dt | None = None,
    ):
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not password_hash:
            raise ValueError("Password hash cannot be empty")

        self.id: UUID = user_id or uuid4()
        self.username: str = username.lower()
        self.password_hash: str = password_hash
        self.role: UserRole = role
        self.is_active: bool = is_active
        self.created_at: dt = created_at or dt.datetime.now(dt.UTC)
        self.updated_at: dt = updated_at or dt.datetime.now(dt.UTC)

    def deactivate(self) -> None:
        """Деактивировать пользователя."""
        self.is_active = False
        self.updated_at = dt.datetime.now(dt.UTC)

    def change_username(self, new_username: str) -> None:
        """Сменить username с валидацией."""
        if not new_username or len(new_username) < 3:
            raise ValueError("Username must be at least 3 characters")
        self.username = new_username.lower()
        self.updated_at = dt.datetime.now(dt.UTC)
