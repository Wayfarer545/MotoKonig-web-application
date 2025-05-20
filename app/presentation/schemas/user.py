# app/presentation/schemas/user.py

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.domain.entities.user import UserRole


class CreateUserSchema(BaseModel):
    username: str = Field(..., min_length=3, description="Уникальное имя пользователя")
    password: str = Field(..., min_length=6, description="Пароль пользователя")
    role: UserRole = Field(UserRole, description="Роль пользователя")


class UpdateUserSchema(BaseModel):
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

    class Config:
        from_attributes = True  # Позволяет возвращать модели SQLAlchemy напрямую
