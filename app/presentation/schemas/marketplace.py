# app/presentation/schemas/marketplace.py
import re
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field, field_validator

from app.domain.value_objects.listing_status import ListingStatus
from app.domain.value_objects.listing_type import ListingType


class BaseModel(_BaseModel):
    """Базовая модель Pydantic с поддержкой атрибутов SQLAlchemy."""
    model_config = ConfigDict(from_attributes=True)


# Схемы для объявлений
class CreateListingSchema(_BaseModel):
    """Схема для создания объявления"""
    category_id: UUID = Field(..., description="ID категории")
    title: str = Field(..., min_length=5, max_length=200, description="Заголовок объявления")
    description: str = Field(..., min_length=20, max_length=5000, description="Описание объявления")
    price: Decimal = Field(..., ge=0, description="Цена")
    listing_type: ListingType = Field(ListingType.SALE, description="Тип объявления")
    location: str | None = Field(None, max_length=200, description="Местоположение")
    latitude: float | None = Field(None, ge=-90, le=90, description="Широта")
    longitude: float | None = Field(None, ge=-180, le=180, description="Долгота")
    contact_phone: str | None = Field(None, max_length=20, description="Контактный телефон")
    contact_email: str | None = Field(None, max_length=100, description="Контактный email")
    is_negotiable: bool = Field(False, description="Торг уместен")
    condition: str | None = Field(None, max_length=50, description="Состояние товара")
    brand: str | None = Field(None, max_length=100, description="Бренд")
    model: str | None = Field(None, max_length=100, description="Модель")
    year: int | None = Field(None, ge=1885, le=2026, description="Год выпуска")
    mileage: int | None = Field(None, ge=0, description="Пробег")

    @field_validator('title', 'description', 'location', 'brand', 'model')
    @classmethod
    def strip_and_validate_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        return stripped if stripped else None

    @field_validator('price')
    @classmethod
    def validate_price(cls, v: Decimal) -> Decimal:
        if v > Decimal('99999999.99'):
            raise ValueError('Price is too large')
        return v


class UpdateListingSchema(_BaseModel):
    """Схема для обновления объявления"""
    title: str | None = Field(None, min_length=5, max_length=200, description="Заголовок объявления")
    description: str | None = Field(None, min_length=20, max_length=5000, description="Описание объявления")
    price: Decimal | None = Field(None, ge=0, description="Цена")
    listing_type: ListingType | None = Field(None, description="Тип объявления")
    location: str | None = Field(None, max_length=200, description="Местоположение")
    latitude: float | None = Field(None, ge=-90, le=90, description="Широта")
    longitude: float | None = Field(None, ge=-180, le=180, description="Долгота")
    contact_phone: str | None = Field(None, max_length=20, description="Контактный телефон")
    contact_email: str | None = Field(None, max_length=100, description="Контактный email")
    is_negotiable: bool | None = Field(None, description="Торг уместен")
    condition: str | None = Field(None, max_length=50, description="Состояние товара")
    brand: str | None = Field(None, max_length=100, description="Бренд")
    model: str | None = Field(None, max_length=100, description="Модель")
    year: int | None = Field(None, ge=1885, le=2026, description="Год выпуска")
    mileage: int | None = Field(None, ge=0, description="Пробег")

    @field_validator('title', 'description', 'location', 'brand', 'model')
    @classmethod
    def strip_and_validate_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        return stripped if stripped else None


class ListingResponseSchema(BaseModel):
    """Схема ответа с данными объявления"""
    id: UUID
    seller_id: UUID
    category_id: UUID
    title: str
    description: str
    price: float
    listing_type: str
    status: str
    location: str | None
    latitude: float | None
    longitude: float | None
    contact_phone: str | None
    contact_email: str | None
    is_negotiable: bool
    condition: str | None
    brand: str | None
    model: str | None
    year: int | None
    mileage: int | None
    is_featured: bool
    views_count: int
    favorites_count: int
    is_active: bool
    is_expired: bool
    expires_at: datetime | None
    created_at: datetime
    updated_at: datetime


class ListingSearchSchema(_BaseModel):
    """Схема для поиска объявлений"""
    query: str | None = Field(None, max_length=200, description="Поисковый запрос")
    category_id: UUID | None = Field(None, description="ID категории")
    min_price: float | None = Field(None, ge=0, description="Минимальная цена")
    max_price: float | None = Field(None, ge=0, description="Максимальная цена")
    location: str | None = Field(None, max_length=200, description="Местоположение")
    brand: str | None = Field(None, max_length=100, description="Бренд")
    model: str | None = Field(None, max_length=100, description="Модель")
    year_from: int | None = Field(None, ge=1885, description="Год от")
    year_to: int | None = Field(None, le=2026, description="Год до")
    condition: str | None = Field(None, max_length=50, description="Состояние")
    listing_type: ListingType | None = Field(None, description="Тип объявления")
    active_only: bool = Field(True, description="Только активные")

    @field_validator('query', 'location', 'brand', 'model')
    @classmethod
    def strip_search_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        return stripped if stripped else None

    @field_validator('max_price')
    @classmethod
    def validate_price_range(cls, v, info):
        if v is not None and 'min_price' in info.data:
            min_price = info.data['min_price']
            if min_price is not None and v < min_price:
                raise ValueError('max_price must be greater than or equal to min_price')
        return v


# Схемы для категорий
class CreateCategorySchema(_BaseModel):
    """Схема для создания категории"""
    name: str = Field(..., min_length=2, max_length=100, description="Название категории")
    slug: str = Field(..., min_length=2, max_length=50, description="URL-slug категории")
    description: str | None = Field(None, max_length=500, description="Описание категории")
    parent_id: UUID | None = Field(None, description="ID родительской категории")
    icon: str | None = Field(None, max_length=100, description="Иконка категории")
    sort_order: int = Field(0, ge=0, description="Порядок сортировки")

    @field_validator('name', 'slug', 'description')
    @classmethod
    def strip_and_validate_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        return stripped if stripped else None

    @field_validator('slug')
    @classmethod
    def validate_slug(cls, v):
        clean_slug = v.strip().lower()
        if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', clean_slug):
            raise ValueError("Slug must contain only lowercase letters, numbers and hyphens")
        return clean_slug


class UpdateCategorySchema(_BaseModel):
    """Схема для обновления категории"""
    name: str | None = Field(None, min_length=2, max_length=100, description="Название категории")
    slug: str | None = Field(None, min_length=2, max_length=50, description="URL-slug категории")
    description: str | None = Field(None, max_length=500, description="Описание категории")
    parent_id: UUID | None = Field(None, description="ID родительской категории")
    icon: str | None = Field(None, max_length=100, description="Иконка категории")
    sort_order: int | None = Field(None, ge=0, description="Порядок сортировки")
    is_active: bool | None = Field(None, description="Активность категории")

    @field_validator('name', 'slug', 'description')
    @classmethod
    def strip_and_validate_strings(cls, v: str | None) -> str | None:
        if v is None:
            return v
        stripped = v.strip()
        return stripped if stripped else None


class CategoryResponseSchema(BaseModel):
    """Схема ответа с данными категории"""
    id: UUID
    name: str
    slug: str
    description: str | None
    parent_id: UUID | None
    icon: str | None
    sort_order: int
    is_active: bool
    is_root_category: bool
    is_subcategory: bool
    created_at: datetime
    updated_at: datetime


# Схемы для изображений объявлений
class AddListingImageSchema(_BaseModel):
    """Схема для добавления изображения к объявлению"""
    media_file_id: UUID = Field(..., description="ID медиафайла")
    alt_text: str | None = Field(None, max_length=200, description="Альтернативный текст")
    is_primary: bool = Field(False, description="Главное изображение")

    @field_validator('alt_text')
    @classmethod
    def strip_alt_text(cls, v: str | None) -> str | None:
        if v is None:
            return v
        return v.strip() if v.strip() else None


class ListingImageResponseSchema(BaseModel):
    """Схема ответа с данными изображения объявления"""
    id: UUID
    listing_id: UUID
    media_file_id: UUID
    url: str
    thumbnail_url: str | None
    alt_text: str | None
    sort_order: int
    is_primary: bool
    width: int | None
    height: int | None
    file_size: int | None
    file_size_mb: float | None
    aspect_ratio: float | None
    created_at: datetime
    updated_at: datetime


class ReorderImagesSchema(_BaseModel):
    """Схема для изменения порядка изображений"""
    image_orders: dict[UUID, int] = Field(..., description="Словарь ID изображения -> новый порядок")

    @field_validator('image_orders')
    @classmethod
    def validate_orders(cls, v):
        for image_id, order in v.items():
            if order < 0:
                raise ValueError(f"Sort order for image {image_id} cannot be negative")
        return v


# Схемы для избранного
class AddToFavoritesSchema(_BaseModel):
    """Схема для добавления в избранное"""
    listing_id: UUID = Field(..., description="ID объявления")


class FavoriteListingResponseSchema(BaseModel):
    """Схема ответа избранного объявления"""
    id: UUID
    user_id: UUID
    listing_id: UUID
    added_at: datetime