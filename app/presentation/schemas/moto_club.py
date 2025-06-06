# app/presentation/schemas/moto_club.py

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field, field_validator

from app.domain.value_objects.club_role import ClubRole


class BaseModel(_BaseModel):
    """Базовая модель Pydantic с поддержкой атрибутов SQLAlchemy."""
    model_config = ConfigDict(from_attributes=True)


class CreateMotoClubSchema(_BaseModel):
    """Схема для создания мотоклуба"""
    name: str = Field(..., min_length=3, max_length=100, description="Название клуба")
    description: str | None = Field(None, max_length=2000, description="Описание клуба")
    is_public: bool = Field(True, description="Публичный ли клуб")
    max_members: int | None = Field(None, gt=0, le=10000, description="Максимальное количество участников")
    location: str | None = Field(None, max_length=200, description="Местоположение клуба")
    website: str | None = Field(None, max_length=500, description="Сайт клуба")

    @field_validator('name', 'location', 'website')
    @classmethod
    def strip_and_validate_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        return stripped if stripped else None

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        return stripped if stripped else None


class UpdateMotoClubSchema(_BaseModel):
    """Схема для обновления мотоклуба"""
    name: str | None = Field(None, min_length=3, max_length=100, description="Название клуба")
    description: str | None = Field(None, max_length=2000, description="Описание клуба")
    is_public: bool | None = Field(None, description="Публичный ли клуб")
    max_members: int | None = Field(None, gt=0, le=10000, description="Максимальное количество участников")
    location: str | None = Field(None, max_length=200, description="Местоположение клуба")
    website: str | None = Field(None, max_length=500, description="Сайт клуба")
    avatar_url: str | None = Field(None, max_length=1000, description="URL аватара клуба")

    @field_validator('name', 'location', 'website', 'avatar_url')
    @classmethod
    def strip_and_validate_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        return stripped if stripped else None


class MotoClubResponseSchema(BaseModel):
    """Схема ответа с данными мотоклуба"""
    id: UUID
    name: str
    description: str | None
    president_id: UUID
    is_public: bool
    max_members: int | None
    location: str | None
    website: str | None
    founded_date: datetime | None
    avatar_url: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime


class JoinClubSchema(_BaseModel):
    """Схема для вступления в клуб"""
    role: ClubRole | None = Field(default=None, description="Запрашиваемая роль (по умолчанию MEMBER)")


class InviteUserSchema(_BaseModel):
    """Схема для приглашения пользователя в клуб"""
    invitee_id: UUID = Field(..., description="ID приглашаемого пользователя")
    invited_role: ClubRole | None = Field(default=None, description="Предлагаемая роль (по умолчанию MEMBER)")
    message: str | None = Field(default=None, max_length=500, description="Персональное сообщение")

    @field_validator('message')
    @classmethod
    def validate_message(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        return stripped if stripped else None


class ClubMembershipResponseSchema(BaseModel):
    """Схема ответа с данными членства в клубе"""
    id: UUID
    club_id: UUID
    user_id: UUID
    role: str
    status: str
    joined_at: datetime
    invited_by: UUID | None
    notes: str | None
    permissions: dict
    created_at: datetime
    updated_at: datetime


class ClubInvitationResponseSchema(BaseModel):
    """Схема ответа с данными приглашения в клуб"""
    id: UUID
    club_id: UUID
    inviter_id: UUID
    invitee_id: UUID
    invited_role: str
    status: str
    message: str | None
    expires_at: datetime
    responded_at: datetime | None
    is_expired: bool
    is_pending: bool
    created_at: datetime
    updated_at: datetime


class MotoClubSearchSchema(_BaseModel):
    """Схема для поиска мотоклубов"""
    name: str | None = Field(None, description="Название для поиска")
    location: str | None = Field(None, description="Местоположение для поиска")
    public_only: bool = Field(False, description="Только публичные клубы")
    active_only: bool = Field(True, description="Только активные клубы")

    @field_validator('name', 'location')
    @classmethod
    def strip_search_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        return stripped if stripped else None
