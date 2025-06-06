# app/presentation/schemas/profile.py

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field, field_validator

from domain.value_objects.privacy_level import PrivacyLevel
from domain.value_objects.social_link import SocialPlatform


class BaseModel(_BaseModel):
    """Базовая модель Pydantic с поддержкой атрибутов SQLAlchemy."""
    model_config = ConfigDict(from_attributes=True)



class CreateProfileSchema(_BaseModel):
    """Схема для создания профиля"""
    bio: str | None = Field(None, max_length=1000, description="Биография")
    location: str | None = Field(None, max_length=200, description="Местоположение")
    phone: str | None = Field(None, max_length=20, description="Телефон")
    date_of_birth: date | None = Field(None, description="Дата рождения")
    riding_experience: int | None = Field(None, ge=0, le=80, description="Опыт вождения в годах")
    privacy_level: PrivacyLevel = Field(PrivacyLevel.PUBLIC, description="Уровень приватности")
    phone_privacy: PrivacyLevel = Field(PrivacyLevel.FRIENDS_ONLY, description="Приватность телефона")
    location_privacy: PrivacyLevel = Field(PrivacyLevel.PUBLIC, description="Приватность локации")

    @field_validator('bio', 'location')
    @classmethod
    def strip_and_validate_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        return stripped if stripped else None

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, v: date | None) -> date | None:
        if v is None:
            return v
        if v >= date.today():
            raise ValueError('Date of birth cannot be in the future')
        # Проверяем минимальный возраст (16 лет)
        age = (date.today() - v).days // 365
        if age < 16:
            raise ValueError('User must be at least 16 years old')
        return v


class UpdateProfileSchema(_BaseModel):
    """Схема для обновления профиля"""
    bio: str | None = Field(None, max_length=1000, description="Биография")
    location: str | None = Field(None, max_length=200, description="Местоположение")
    phone: str | None = Field(None, max_length=20, description="Телефон")
    date_of_birth: date | None = Field(None, description="Дата рождения")
    riding_experience: int | None = Field(None, ge=0, le=80, description="Опыт вождения в годах")
    privacy_level: PrivacyLevel | None = Field(None, description="Уровень приватности")
    phone_privacy: PrivacyLevel | None = Field(None, description="Приватность телефона")
    location_privacy: PrivacyLevel | None = Field(None, description="Приватность локации")

    @field_validator('bio', 'location')
    @classmethod
    def strip_and_validate_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        return stripped if stripped else None

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls, v: date | None) -> date | None:
        if v is None:
            return v
        if v >= date.today():
            raise ValueError('Date of birth cannot be in the future')
        age = (date.today() - v).days // 365
        if age < 16:
            raise ValueError('User must be at least 16 years old')
        return v


class ProfileResponseSchema(BaseModel):
    """Схема ответа с данными профиля"""
    id: UUID
    user_id: UUID
    bio: str | None
    location: str | None
    phone: str | None  # Может быть None в зависимости от приватности
    date_of_birth: str | None  # ISO формат
    age: int | None
    riding_experience: int | None
    avatar_url: str | None
    privacy_level: str
    created_at: datetime
    updated_at: datetime


class AddSocialLinkSchema(_BaseModel):
    """Схема для добавления социальной ссылки"""
    platform: SocialPlatform = Field(..., description="Социальная платформа")
    url: str = Field(..., max_length=500, description="URL или username")
    privacy_level: PrivacyLevel = Field(PrivacyLevel.FRIENDS_ONLY, description="Уровень приватности")

    @field_validator('url')
    @classmethod
    def validate_url(cls, v: str) -> str:
        return v.strip()


class SocialLinkResponseSchema(BaseModel):
    """Схема ответа с данными социальной ссылки"""
    id: UUID | None  # Может быть None если не видна
    profile_id: UUID | None
    platform: str
    url: str | None  # Может быть None в зависимости от приватности
    display_name: str
    privacy_level: str
    is_verified: bool | None
    visible: bool
    created_at: datetime | None
    updated_at: datetime | None