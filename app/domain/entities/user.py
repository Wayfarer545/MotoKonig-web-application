# app/domain/entities/user.py

from __future__ import annotations

from enum import IntEnum
from uuid import UUID, uuid4
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.presentation.schemas.user import UserResponseSchema


class UserRole(IntEnum):
    ADMIN = 0
    OPERATOR = 1
    USER = 2


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
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
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
        self.created_at: datetime | None = created_at
        self.updated_at: datetime | None = updated_at

    def deactivate(self) -> None:
        """Деактивировать пользователя."""
        self.is_active = False

    def change_username(self, new_username: str) -> None:
        """Сменить username с валидацией."""
        if not new_username or len(new_username) < 3:
            raise ValueError("Username must be at least 3 characters")
        self.username = new_username.lower()

    def to_dto(self) -> dict:
        """Конвертировать в DTO для API"""
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }