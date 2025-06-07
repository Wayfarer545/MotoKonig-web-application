# app/infrastructure/models/listing_model.py

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import Boolean, Enum as SQLEnum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.value_objects.listing_status import ListingStatus
from app.domain.value_objects.listing_type import ListingType

__all__ = ["Listing"]

if TYPE_CHECKING:
    from .listing_category_model import ListingCategory
    from .listing_image_model import ListingImage
    from .user_model import User


class Listing(UUIDAuditBase):
    """SQLAlchemy модель объявления"""

    __tablename__ = "listings"

    # Связи
    seller_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    seller: Mapped["User"] = relationship("User", lazy="selectin")

    category_id: Mapped[str] = mapped_column(
        ForeignKey("listing_categories.id"),
        nullable=False,
        index=True
    )
    category: Mapped["ListingCategory"] = relationship("ListingCategory", back_populates="listings")

    # Основная информация
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, index=True)

    # Тип и статус
    listing_type: Mapped[ListingType] = mapped_column(
        SQLEnum(ListingType, name="listing_type", native_enum=False),
        nullable=False,
        index=True
    )
    status: Mapped[ListingStatus] = mapped_column(
        SQLEnum(ListingStatus, name="listing_status", native_enum=False),
        nullable=False,
        default=ListingStatus.DRAFT,
        index=True
    )

    # Геолокация
    location: Mapped[str | None] = mapped_column(String(200), nullable=True, index=True)
    latitude: Mapped[float | None] = mapped_column(Numeric(10, 8), nullable=True)
    longitude: Mapped[float | None] = mapped_column(Numeric(11, 8), nullable=True)

    # Контакты
    contact_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    contact_email: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Дополнительные поля
    is_negotiable: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    condition: Mapped[str | None] = mapped_column(String(50), nullable=True)
    brand: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    mileage: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Статистика
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    views_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    favorites_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Время действия
    expires_at: Mapped[str | None] = mapped_column(String(50), nullable=True, index=True)

    # Связь с изображениями
    images: Mapped[list["ListingImage"]] = relationship(
        "ListingImage",
        back_populates="listing",
        cascade="all, delete-orphan",
        order_by="ListingImage.sort_order"
    )