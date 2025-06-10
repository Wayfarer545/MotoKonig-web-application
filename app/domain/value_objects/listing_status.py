# app/domain/value_objects/listing_status.py

from enum import Enum


class ListingStatus(Enum):
    """Статусы объявлений в маркетплейсе"""
    DRAFT = "draft"  # Черновик
    MODERATION = "moderation"  # На модерации
    ACTIVE = "active"  # Активное
    SOLD = "sold"  # Продано
    EXPIRED = "expired"  # Истек срок
    REJECTED = "rejected"  # Отклонено модерацией
    SUSPENDED = "suspended"  # Приостановлено

    def get_display_name(self) -> str:
        """Получить отображаемое название статуса"""
        display_names = {
            ListingStatus.DRAFT: "Черновик",
            ListingStatus.MODERATION: "На модерации",
            ListingStatus.ACTIVE: "Активное",
            ListingStatus.SOLD: "Продано",
            ListingStatus.EXPIRED: "Истёк срок",
            ListingStatus.REJECTED: "Отклонено",
            ListingStatus.SUSPENDED: "Приостановлено",
        }
        return display_names[self]

    def is_visible_to_public(self) -> bool:
        """Видно ли объявление публично"""
        return self in [ListingStatus.ACTIVE]

    def is_editable(self) -> bool:
        """Можно ли редактировать объявление"""
        return self in [ListingStatus.DRAFT, ListingStatus.REJECTED]

    def can_be_activated(self) -> bool:
        """Может ли быть активировано"""
        return self in [ListingStatus.DRAFT, ListingStatus.REJECTED, ListingStatus.SUSPENDED]
