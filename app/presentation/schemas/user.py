# app/presentation/schemas/user.py

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field

from app.domain.value_objects.user_role import UserRole


class BaseModel(_BaseModel):
    """Базовая модель Pydantic с поддержкой атрибутов SQLAlchemy."""
    model_config = ConfigDict(from_attributes=True)



class CreateUserSchema(_BaseModel):
    username: str = Field(..., min_length=3, description="Уникальное имя пользователя")
    password: str = Field(..., min_length=6, description="Пароль пользователя")
    role: UserRole = Field(default=UserRole.USER, description="Роль пользователя")


class UpdateUserSchema(_BaseModel):
    username: str | None = Field(None, min_length=3, description="Новое имя пользователя")
    password: str | None = Field(None, min_length=6, description="Новый пароль")
    role: UserRole | None = Field(None, description="Новая роль пользователя")
    deactivate: bool = Field(False, description="Флаг деактивации пользователя")


class UserResponseSchema(BaseModel):
    id: UUID
    username: str
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: datetime

