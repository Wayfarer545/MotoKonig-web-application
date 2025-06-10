# app/presentation/schemas/listing.py

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field, field_validator

from app.domain.value_objects.listing_category import ListingCategory
from app.domain.value_objects.listing_status import ListingStatus


class BaseModel(_BaseModel):
    """Базовая модель Pydantic с поддержкой атрибутов SQLAlchemy."""
    model_config = ConfigDict(from_attributes=True)


class CreateListingSchema(_BaseModel):
    """Схема для создания объявления"""
    title: str = Field(..., min_length=5, max_length=100, description="Название объявления")
    description: str = Field(..., min_length=20, max_length=5000, description="Описание")
    category: ListingCategory = Field(..., description="Категория товара")
    price: int = Field(..., ge=0, description="Цена в копейках")
    location: str = Field(..., min_length=1, max_length=200, description="Местоположение")
    is_negotiable: bool = Field(True, description="Торг уместен")
    contact_phone: str | None = Field(None, max_length=20, description="Контактный телефон")
    contact_email: str | None = Field(None, max_length=100, description="Контактный email")
    photo_urls: list[str] | None = Field(None, max_items=5, description="URL фотографий")

    @field_validator('title', 'description', 'location')
    @classmethod
    def strip_strings(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()

    @field_validator('contact_phone')
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        if v is None:
            return v
        import re
        phone_pattern = r'^\+?[1-9]\d{6,14}$'
        if not re.match(phone_pattern, v.replace(' ', '').replace('-', '')):
            raise ValueError('Invalid phone number format')
        return v.strip()

    @field_validator('photo_urls')
    @classmethod
    def validate_photos(cls, v: list[str] | None) -> list[str] | None:
        if v is None:
            return v
        if len(v) > 5:
            raise ValueError('Maximum 5 photos allowed')
        return v


class UpdateListingSchema(_BaseModel):
    """Схема для обновления объявления"""
    title: str | None = Field(None, min_length=5, max_length=100, description="Название объявления")
    description: str | None = Field(None, min_length=20, max_length=5000, description="Описание")
    category: ListingCategory | None = Field(None, description="Категория товара")
    price: int | None = Field(None, ge=0, description="Цена в копейках")
    location: str | None = Field(None, min_length=1, max_length=200, description="Местоположение")
    is_negotiable: bool | None = Field(None, description="Торг уместен")
    contact_phone: str | None = Field(None, max_length=20, description="Контактный телефон")
    contact_email: str | None = Field(None, max_length=100, description="Контактный email")

    @field_validator('title', 'description', 'location')
    @classmethod
    def strip_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()


class ListingResponseSchema(BaseModel):
    """Схема ответа с данными объявления"""
    id: UUID
    seller_id: UUID
    title: str
    description: str
    category: str
    category_display: str
    price: int
    price_formatted: str
    currency: str
    location: str
    status: str
    status_display: str
    is_negotiable: bool
    photo_urls: list[str]
    views_count: int
    expires_at: datetime | None
    is_featured: bool
    is_expired: bool
    is_visible: bool
    created_at: datetime
    updated_at: datetime


class ListingDetailResponseSchema(ListingResponseSchema):
    """Расширенная схема с приватной информацией"""
    contact_phone: str | None
    contact_email: str | None
    moderation_notes: str | None


class ListingSearchSchema(_BaseModel):
    """Схема для поиска объявлений"""
    category: ListingCategory | None = Field(None, description="Категория для поиска")
    location: str | None = Field(None, description="Местоположение для поиска")
    price_min: int | None = Field(None, ge=0, description="Минимальная цена в копейках")
    price_max: int | None = Field(None, ge=0, description="Максимальная цена в копейках")
    search_query: str | None = Field(None, description="Поисковый запрос")
    seller_id: UUID | None = Field(None, description="ID продавца")
    featured_first: bool = Field(True, description="Показывать рекомендуемые первыми")

    @field_validator('location', 'search_query')
    @classmethod
    def strip_search_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        return stripped if stripped else None


class FavoriteResponseSchema(BaseModel):
    """Схема ответа для избранного"""
    id: UUID
    user_id: UUID
    listing_id: UUID
    created_at: datetime


class MessageResponseSchema(BaseModel):
    """Схема ответа с сообщением"""
    message: str = Field(..., description="Сообщение о результате операции")