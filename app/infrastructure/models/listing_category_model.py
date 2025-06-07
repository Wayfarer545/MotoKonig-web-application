# app/infrastructure/models/listing_category_model.py

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

__all__ = ["ListingCategory"]

if TYPE_CHECKING:
    from .listing_model import Listing


class ListingCategory(UUIDAuditBase):
    """SQLAlchemy модель категории объявлений"""

    __tablename__ = "listing_categories"

    # Основная информация
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Иерархия категорий
    parent_id: Mapped[str | None] = mapped_column(
        ForeignKey("listing_categories.id"),
        nullable=True,
        index=True
    )
    parent: Mapped["ListingCategory"] = relationship(
        "ListingCategory",
        remote_side="ListingCategory.id",
        back_populates="children"
    )
    children: Mapped[list["ListingCategory"]] = relationship(
        "ListingCategory",
        back_populates="parent",
        cascade="all, delete-orphan"
    )

    # Настройки отображения
    icon: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False, index=True)

    # Связь с объявлениями
    listings: Mapped[list["Listing"]] = relationship(
        "Listing",
        back_populates="category",
        cascade="all, delete-orphan"
    )