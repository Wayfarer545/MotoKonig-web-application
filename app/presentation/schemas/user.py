# app/presentation/schemas/user.py

from datetime import datetime
from enum import IntEnum
from uuid import UUID

from pydantic import BaseModel as _BaseModel, Field, ConfigDict


class UserRole(IntEnum):
    ADMIN = 0
    OPERATOR = 1
    USER = 2


class BaseModel(_BaseModel):
    """Базовая модель Pydantic с поддержкой атрибутов SQLAlchemy."""
    model_config = ConfigDict(from_attributes=True)



class CreateUserSchema(BaseModel):
    username: str = Field(..., min_length=3, description="Уникальное имя пользователя")
    password: str = Field(..., min_length=6, description="Пароль пользователя")
    role: UserRole = Field(UserRole, description="Роль пользователя")


class UpdateUserSchema(BaseModel):
    username: str | None = Field(None, min_length=3, description="Новое имя пользователя")
    password: str | None = Field(None, min_length=6, description="Новый пароль")
    role: UserRole | None = Field(None, description="Новая роль пользователя")
    deactivate: bool = Field(False, description="Флаг деактивации пользователя")


class UserResponseSchema(_BaseModel):
    id: UUID
    username: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

