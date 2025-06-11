# app/presentation/schemas/motokonig.py

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field, field_validator

from app.domain.value_objects.achievement_type import AchievementType
from app.domain.value_objects.motokonig_status import MotoKonigStatus


class BaseModel(_BaseModel):
    """Базовая модель Pydantic с поддержкой атрибутов SQLAlchemy."""
    model_config = ConfigDict(from_attributes=True)


class CreateMotoKonigProfileSchema(_BaseModel):
    """Схема для создания профиля MotoKonig"""
    nickname: str = Field(..., min_length=3, max_length=30, description="Уникальный никнейм")
    bio: str | None = Field(None, max_length=1000, description="Биография")
    avatar_url: str | None = Field(None, max_length=500, description="URL аватара")
    is_public: bool = Field(True, description="Публичный профиль")

    @field_validator('nickname')
    @classmethod
    def validate_nickname(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Nickname cannot be empty")
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Nickname can only contain letters, numbers, - and _")
        return v


class UpdateMotoKonigProfileSchema(_BaseModel):
    """Схема для обновления профиля MotoKonig"""
    nickname: str | None = Field(None, min_length=3, max_length=30)
    bio: str | None = Field(None, max_length=1000)
    avatar_url: str | None = Field(None, max_length=500)
    is_public: bool | None = Field(None)


class AchievementResponseSchema(BaseModel):
    """Схема ответа для достижения"""
    achievement_id: UUID
    achievement_type: AchievementType
    earned_at: datetime
    description: str | None
    metadata: dict | None = None


class MotoKonigResponseSchema(BaseModel):
    """Схема ответа для профиля MotoKonig"""
    motokonig_id: UUID
    user_id: UUID
    nickname: str
    status: MotoKonigStatus
    experience_points: int
    total_distance: int
    total_rides: int
    average_speed: float | None
    max_speed: float | None
    rating: float
    bio: str | None
    avatar_url: str | None
    is_public: bool
    achievements: list[AchievementResponseSchema]
    created_at: datetime
    updated_at: datetime


class MotoKonigListItemSchema(BaseModel):
    """Схема элемента списка MotoKonig"""
    motokonig_id: UUID
    nickname: str
    status: MotoKonigStatus
    rating: float
    total_distance: int
    avatar_url: str | None


class UpdateRideStatsSchema(_BaseModel):
    """Схема для обновления статистики поездки"""
    distance: int = Field(..., gt=0, description="Пройденное расстояние в км")
    duration: int = Field(..., gt=0, description="Продолжительность в минутах")
    max_speed: float = Field(..., gt=0, le=400, description="Максимальная скорость")
