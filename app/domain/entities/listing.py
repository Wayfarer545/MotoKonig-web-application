# app/domain/entities/listing.py

from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.domain.value_objects.listing_category import ListingCategory
from app.domain.value_objects.listing_status import ListingStatus

if TYPE_CHECKING:
    pass


class Listing:
    """
    Доменная сущность объявления в маркетплейсе

    Инварианты:
    - Название не может быть пустым
    - Цена должна быть положительной для платных объявлений
    - Максимум 5 фотографий на объявление
    - Максимум 100 активных объявлений на пользователя
    - Описание не должно быть слишком длинным
    """

    def __init__(
            self,
            *,
            listing_id: UUID | None = None,
            seller_id: UUID,
            title: str,
            description: str,
            category: ListingCategory,
            price: int,  # в копейках для точности
            currency: str = "RUB",
            location: str,
            status: ListingStatus = ListingStatus.DRAFT,
            is_negotiable: bool = True,
            contact_phone: str | None = None,
            contact_email: str | None = None,
            photo_urls: list[str] | None = None,
            views_count: int = 0,
            expires_at: datetime | None = None,
            moderation_notes: str | None = None,
            is_featured: bool = False,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ):
        # Валидация инвариантов
        self._validate_title(title)
        self._validate_description(description)
        self._validate_price(price)
        self._validate_location(location)
        if photo_urls:
            self._validate_photo_urls(photo_urls)
        if contact_phone:
            self._validate_contact_phone(contact_phone)

        self.id: UUID = listing_id or uuid4()
        self.seller_id: UUID = seller_id
        self.title: str = title.strip()
        self.description: str = description.strip()
        self.category: ListingCategory = category
        self.price: int = price
        self.currency: str = currency
        self.location: str = location.strip()
        self.status: ListingStatus = status
        self.is_negotiable: bool = is_negotiable
        self.contact_phone: str | None = contact_phone.strip() if contact_phone else None
        self.contact_email: str | None = contact_email.strip() if contact_email else None
        self.photo_urls: list[str] = photo_urls or []
        self.views_count: int = views_count
        self.expires_at: datetime | None = expires_at or (datetime.utcnow() + timedelta(days=30))
        self.moderation_notes: str | None = moderation_notes
        self.is_featured: bool = is_featured
        self.created_at: datetime | None = created_at
        self.updated_at: datetime | None = updated_at

    def _validate_title(self, title: str) -> None:
        """Валидация названия объявления"""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title.strip()) < 5:
            raise ValueError("Title must be at least 5 characters long")
        if len(title.strip()) > 100:
            raise ValueError("Title cannot be longer than 100 characters")

    def _validate_description(self, description: str) -> None:
        """Валидация описания"""
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")
        if len(description.strip()) < 20:
            raise ValueError("Description must be at least 20 characters long")
        if len(description.strip()) > 5000:
            raise ValueError("Description cannot be longer than 5000 characters")

    def _validate_price(self, price: int) -> None:
        """Валидация цены"""
        if price < 0:
            raise ValueError("Price cannot be negative")
        if price > 100_000_000_00:  # 100 млн рублей в копейках
            raise ValueError("Price is too high")

    def _validate_location(self, location: str) -> None:
        """Валидация локации"""
        if not location or not location.strip():
            raise ValueError("Location cannot be empty")
        if len(location.strip()) > 200:
            raise ValueError("Location cannot be longer than 200 characters")

    def _validate_photo_urls(self, photo_urls: list[str]) -> None:
        """Валидация фотографий"""
        if len(photo_urls) > 5:
            raise ValueError("Maximum 5 photos allowed per listing")

    def _validate_contact_phone(self, phone: str) -> None:
        """Валидация телефона"""
        import re
        phone_pattern = r'^\+?[1-9]\d{6,14}$'
        if not re.match(phone_pattern, phone.replace(' ', '').replace('-', '')):
            raise ValueError("Invalid phone number format")

    def update_title(self, title: str) -> None:
        """Обновить название"""
        if not self.status.is_editable():
            raise ValueError("Cannot edit listing in current status")
        self._validate_title(title)
        self.title = title.strip()

    def update_description(self, description: str) -> None:
        """Обновить описание"""
        if not self.status.is_editable():
            raise ValueError("Cannot edit listing in current status")
        self._validate_description(description)
        self.description = description.strip()

    def update_price(self, price: int) -> None:
        """Обновить цену"""
        if not self.status.is_editable():
            raise ValueError("Cannot edit listing in current status")
        self._validate_price(price)
        self.price = price

    def add_photo(self, photo_url: str) -> None:
        """Добавить фотографию"""
        if len(self.photo_urls) >= 5:
            raise ValueError("Maximum 5 photos allowed")
        if photo_url not in self.photo_urls:
            self.photo_urls.append(photo_url)

    def remove_photo(self, photo_url: str) -> None:
        """Удалить фотографию"""
        if photo_url in self.photo_urls:
            self.photo_urls.remove(photo_url)

    def submit_for_moderation(self) -> None:
        """Отправить на модерацию"""
        if not self.status.can_be_activated():
            raise ValueError("Cannot submit listing in current status")
        self.status = ListingStatus.MODERATION
        self.moderation_notes = None

    def approve(self) -> None:
        """Одобрить объявление"""
        if self.status != ListingStatus.MODERATION:
            raise ValueError("Can only approve listings in moderation")
        self.status = ListingStatus.ACTIVE

    def reject(self, reason: str) -> None:
        """Отклонить объявление"""
        if self.status != ListingStatus.MODERATION:
            raise ValueError("Can only reject listings in moderation")
        self.status = ListingStatus.REJECTED
        self.moderation_notes = reason

    def mark_as_sold(self) -> None:
        """Пометить как проданное"""
        if self.status != ListingStatus.ACTIVE:
            raise ValueError("Can only mark active listings as sold")
        self.status = ListingStatus.SOLD

    def suspend(self, reason: str | None = None) -> None:
        """Приостановить объявление"""
        if self.status != ListingStatus.ACTIVE:
            raise ValueError("Can only suspend active listings")
        self.status = ListingStatus.SUSPENDED
        if reason:
            self.moderation_notes = reason

    def reactivate(self) -> None:
        """Переактивировать объявление"""
        if self.status != ListingStatus.SUSPENDED:
            raise ValueError("Can only reactivate suspended listings")
        if self.is_expired():
            raise ValueError("Cannot reactivate expired listing")
        self.status = ListingStatus.ACTIVE

    def extend_expiry(self, days: int = 30) -> None:
        """Продлить срок действия"""
        if days <= 0 or days > 90:
            raise ValueError("Extension must be between 1 and 90 days")
        self.expires_at = datetime.utcnow() + timedelta(days=days)
        if self.status == ListingStatus.EXPIRED:
            self.status = ListingStatus.ACTIVE

    def increment_views(self) -> None:
        """Увеличить счетчик просмотров"""
        self.views_count += 1

    def make_featured(self) -> None:
        """Сделать рекомендуемым"""
        self.is_featured = True

    def remove_featured(self) -> None:
        """Убрать из рекомендуемых"""
        self.is_featured = False

    def is_expired(self) -> bool:
        """Проверить, истёк ли срок"""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at

    def get_price_rub(self) -> float:
        """Получить цену в рублях"""
        return self.price / 100.0

    def get_formatted_price(self) -> str:
        """Получить отформатированную цену"""
        if self.price == 0:
            return "Договорная"
        price_rub = self.get_price_rub()
        return f"{price_rub:,.0f} ₽".replace(',', ' ')

    def is_visible_to_public(self) -> bool:
        """Видно ли объявление публично"""
        return self.status.is_visible_to_public() and not self.is_expired()

    def can_be_contacted(self) -> bool:
        """Можно ли связаться с продавцом"""
        return self.is_visible_to_public() and (self.contact_phone or self.contact_email)

    def to_dto(self, include_private_info: bool = False) -> dict:
        """Конвертировать в DTO для API"""
        dto = {
            "id": self.id,
            "seller_id": self.seller_id,
            "title": self.title,
            "description": self.description,
            "category": self.category.value,
            "category_display": self.category.get_display_name(),
            "price": self.price,
            "price_formatted": self.get_formatted_price(),
            "currency": self.currency,
            "location": self.location,
            "status": self.status.value,
            "status_display": self.status.get_display_name(),
            "is_negotiable": self.is_negotiable,
            "photo_urls": self.photo_urls,
            "views_count": self.views_count,
            "expires_at": self.expires_at,
            "is_featured": self.is_featured,
            "is_expired": self.is_expired(),
            "is_visible": self.is_visible_to_public(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

        # Приватная информация только для владельца и админов
        if include_private_info:
            dto.update({
                "contact_phone": self.contact_phone,
                "contact_email": self.contact_email,
                "moderation_notes": self.moderation_notes,
            })

        return dto