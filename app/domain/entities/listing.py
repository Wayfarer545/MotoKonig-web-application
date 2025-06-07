# app/domain/entities/listing.py

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.domain.value_objects.listing_status import ListingStatus
from app.domain.value_objects.listing_type import ListingType

if TYPE_CHECKING:
    pass


class Listing:
    """
    Доменная сущность объявления в маркетплейсе

    Инварианты:
    - Цена не может быть отрицательной
    - Заголовок не может быть пустым
    - Описание не может быть слишком длинным
    - Контакты должны быть валидными
    """

    def __init__(
            self,
            *,
            listing_id: UUID | None = None,
            seller_id: UUID,
            category_id: UUID,
            title: str,
            description: str,
            price: Decimal,
            listing_type: ListingType = ListingType.SALE,
            location: str | None = None,
            latitude: float | None = None,
            longitude: float | None = None,
            contact_phone: str | None = None,
            contact_email: str | None = None,
            is_negotiable: bool = False,
            condition: str | None = None,
            brand: str | None = None,
            model: str | None = None,
            year: int | None = None,
            mileage: int | None = None,
            status: ListingStatus = ListingStatus.DRAFT,
            is_featured: bool = False,
            views_count: int = 0,
            favorites_count: int = 0,
            expires_at: datetime | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ):
        # Валидация инвариантов
        self._validate_title(title)
        self._validate_description(description)
        self._validate_price(price)
        if contact_phone is not None:
            self._validate_phone(contact_phone)
        if contact_email is not None:
            self._validate_email(contact_email)
        if year is not None:
            self._validate_year(year)
        if mileage is not None:
            self._validate_mileage(mileage)
        if latitude is not None and longitude is not None:
            self._validate_coordinates(latitude, longitude)

        self.id: UUID = listing_id or uuid4()
        self.seller_id: UUID = seller_id
        self.category_id: UUID = category_id
        self.title: str = title.strip()
        self.description: str = description.strip()
        self.price: Decimal = price
        self.listing_type: ListingType = listing_type
        self.location: str | None = location.strip() if location else None
        self.latitude: float | None = latitude
        self.longitude: float | None = longitude
        self.contact_phone: str | None = contact_phone.strip() if contact_phone else None
        self.contact_email: str | None = contact_email.strip().lower() if contact_email else None
        self.is_negotiable: bool = is_negotiable
        self.condition: str | None = condition.strip() if condition else None
        self.brand: str | None = brand.strip().title() if brand else None
        self.model: str | None = model.strip() if model else None
        self.year: int | None = year
        self.mileage: int | None = mileage
        self.status: ListingStatus = status
        self.is_featured: bool = is_featured
        self.views_count: int = views_count
        self.favorites_count: int = favorites_count
        self.expires_at: datetime | None = expires_at
        self.created_at: datetime | None = created_at
        self.updated_at: datetime | None = updated_at

    def _validate_title(self, title: str) -> None:
        """Валидация заголовка"""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title.strip()) < 5:
            raise ValueError("Title must be at least 5 characters long")
        if len(title.strip()) > 200:
            raise ValueError("Title cannot be longer than 200 characters")

    def _validate_description(self, description: str) -> None:
        """Валидация описания"""
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")
        if len(description.strip()) < 20:
            raise ValueError("Description must be at least 20 characters long")
        if len(description.strip()) > 5000:
            raise ValueError("Description cannot be longer than 5000 characters")

    def _validate_price(self, price: Decimal) -> None:
        """Валидация цены"""
        if price < 0:
            raise ValueError("Price cannot be negative")
        if price > Decimal('99999999.99'):
            raise ValueError("Price is too large")

    def _validate_phone(self, phone: str) -> None:
        """Валидация телефона"""
        import re
        phone_pattern = r'^\+?[1-9]\d{6,14}$'
        clean_phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        if not re.match(phone_pattern, clean_phone):
            raise ValueError("Invalid phone number format")

    def _validate_email(self, email: str) -> None:
        """Валидация email"""
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email.strip()):
            raise ValueError("Invalid email format")

    def _validate_year(self, year: int) -> None:
        """Валидация года"""
        current_year = datetime.now().year
        if year < 1885:
            raise ValueError("Year cannot be before 1885")
        if year > current_year + 1:
            raise ValueError(f"Year cannot be in the future (max: {current_year + 1})")

    def _validate_mileage(self, mileage: int) -> None:
        """Валидация пробега"""
        if mileage < 0:
            raise ValueError("Mileage cannot be negative")
        if mileage > 10000000:  # 10 млн км - разумный максимум
            raise ValueError("Mileage seems unrealistic")

    def _validate_coordinates(self, latitude: float, longitude: float) -> None:
        """Валидация координат"""
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180")

    def publish(self) -> None:
        """Опубликовать объявление"""
        if self.status != ListingStatus.DRAFT:
            raise ValueError("Can only publish draft listings")
        self.status = ListingStatus.ACTIVE
        # Устанавливаем срок действия (30 дней по умолчанию)
        if not self.expires_at:
            from datetime import timedelta
            self.expires_at = datetime.utcnow() + timedelta(days=30)

    def deactivate(self) -> None:
        """Деактивировать объявление"""
        if self.status not in [ListingStatus.ACTIVE, ListingStatus.FEATURED]:
            raise ValueError("Can only deactivate active listings")
        self.status = ListingStatus.INACTIVE

    def archive(self) -> None:
        """Архивировать объявление"""
        self.status = ListingStatus.ARCHIVED

    def mark_as_sold(self) -> None:
        """Пометить как проданное"""
        if self.listing_type != ListingType.SALE:
            raise ValueError("Can only mark sale listings as sold")
        self.status = ListingStatus.SOLD

    def feature(self) -> None:
        """Сделать объявление рекомендуемым"""
        if self.status != ListingStatus.ACTIVE:
            raise ValueError("Can only feature active listings")
        self.status = ListingStatus.FEATURED
        self.is_featured = True

    def unfeature(self) -> None:
        """Убрать из рекомендуемых"""
        if self.status == ListingStatus.FEATURED:
            self.status = ListingStatus.ACTIVE
        self.is_featured = False

    def increment_views(self) -> None:
        """Увеличить счетчик просмотров"""
        self.views_count += 1

    def increment_favorites(self) -> None:
        """Увеличить счетчик избранного"""
        self.favorites_count += 1

    def decrement_favorites(self) -> None:
        """Уменьшить счетчик избранного"""
        if self.favorites_count > 0:
            self.favorites_count -= 1

    def update_title(self, title: str) -> None:
        """Обновить заголовок"""
        self._validate_title(title)
        self.title = title.strip()

    def update_description(self, description: str) -> None:
        """Обновить описание"""
        self._validate_description(description)
        self.description = description.strip()

    def update_price(self, price: Decimal) -> None:
        """Обновить цену"""
        self._validate_price(price)
        self.price = price

    def update_location(self, location: str | None, latitude: float | None = None, longitude: float | None = None) -> None:
        """Обновить локацию"""
        if latitude is not None and longitude is not None:
            self._validate_coordinates(latitude, longitude)
        self.location = location.strip() if location else None
        self.latitude = latitude
        self.longitude = longitude

    def is_active(self) -> bool:
        """Проверить, активно ли объявление"""
        return self.status in [ListingStatus.ACTIVE, ListingStatus.FEATURED]

    def is_expired(self) -> bool:
        """Проверить, истекло ли объявление"""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at

    def extend_expiry(self, days: int = 30) -> None:
        """Продлить срок действия"""
        from datetime import timedelta
        if self.expires_at:
            self.expires_at = max(self.expires_at, datetime.utcnow()) + timedelta(days=days)
        else:
            self.expires_at = datetime.utcnow() + timedelta(days=days)

    def to_dto(self) -> dict:
        """Конвертировать в DTO для API"""
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "category_id": self.category_id,
            "title": self.title,
            "description": self.description,
            "price": float(self.price),
            "listing_type": self.listing_type.value,
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "contact_phone": self.contact_phone,
            "contact_email": self.contact_email,
            "is_negotiable": self.is_negotiable,
            "condition": self.condition,
            "brand": self.brand,
            "model": self.model,
            "year": self.year,
            "mileage": self.mileage,
            "status": self.status.value,
            "is_featured": self.is_featured,
            "views_count": self.views_count,
            "favorites_count": self.favorites_count,
            "is_active": self.is_active(),
            "is_expired": self.is_expired(),
            "expires_at": self.expires_at,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }