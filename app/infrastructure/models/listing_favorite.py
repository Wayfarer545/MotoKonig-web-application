# app/infrastructure/models/listing_favorite.py

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

__all__ = ["ListingFavorite"]

if TYPE_CHECKING:
    from .listing import Listing
    from .user import User


class ListingFavorite(UUIDAuditBase):
    """SQLAlchemy модель избранного объявления"""

    __tablename__ = "listing_favorites"
    __table_args__ = (
        # Уникальная комбинация пользователь + объявление
        UniqueConstraint('user_id', 'listing_id', name='uq_user_listing_favorite'),
    )

    # Связи
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    user: Mapped["User"] = relationship("User", lazy="selectin")

    listing_id: Mapped[str] = mapped_column(
        ForeignKey("listings.id"),
        nullable=False,
        index=True
    )
    listing: Mapped["Listing"] = relationship("Listing", back_populates="favorites")