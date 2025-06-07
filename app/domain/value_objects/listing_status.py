# app/domain/value_objects/listing_status.py

from enum import Enum


class ListingStatus(Enum):
    """Статусы объявлений"""
    DRAFT = "draft"          # Черновик
    ACTIVE = "active"        # Активное
    FEATURED = "featured"    # Рекомендуемое
    INACTIVE = "inactive"    # Неактивное
    EXPIRED = "expired"      # Истекшее
    SOLD = "sold"           # Продано
    ARCHIVED = "archived"    # Архивировано
    MODERATION = "moderation"  # На модерации
    REJECTED = "rejected"    # Отклонено модерацией