# app/infrastructure/models/listing.py

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects.listing_category import ListingCategory
from app.domain.value_objects.listing_status import ListingStatus

__all__ = ["Listing"]

if TYPE_CHECKING:
    from .listing_favorite import ListingFavorite
    from .user import User


class Listing(UUIDAuditBase):
    """SQLAlchemy модель объявления"""

    __tablename__ = "listings"

    # Связь с продавцом
    seller_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    seller: Mapped["User"] = relationship("User", lazy="selectin")

    # Основная информация
    title: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[ListingCategory] = mapped_column(
        SQLEnum(ListingCategory, name="listing_category", native_enum=False),
        nullable=False,
        index=True
    )

    # Цена и торговля
    price: Mapped[int] = mapped_column(Integer, nullable=False, index=True)  # в копейках
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="RUB")
    is_negotiable: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Локация
    location: Mapped[str] = mapped_column(String(200), nullable=False, index=True)

    # Статус и модерация
    status: Mapped[ListingStatus] = mapped_column(
        SQLEnum(ListingStatus, name="listing_status", native_enum=False),
        nullable=False,
        default=ListingStatus.DRAFT,
        index=True
    )
    moderation_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Контактная информация
    contact_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Медиа (JSON массив URL'ов)
    photo_urls: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON

    # Статистика
    views_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_featured: Mapped[bool] = mapped_column(default=False, nullable=False, index=True)

    # Сроки
    expires_at: Mapped[str | None] = mapped_column(String(50), nullable=True)  # ISO формат

    # Связи
    favorites: Mapped[list["ListingFavorite"]] = relationship(
        "ListingFavorite",
        back_populates="listing",
        cascade="all, delete-orphan",
        lazy="selectin"
    )