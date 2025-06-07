# app/infrastructure/models/listing_image_model.py

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

__all__ = ["ListingImage"]

if TYPE_CHECKING:
    from .listing_model import Listing
    from .media_file_model import MediaFile


class ListingImage(UUIDAuditBase):
    """SQLAlchemy модель изображения объявления"""

    __tablename__ = "listing_images"

    # Связи
    listing_id: Mapped[str] = mapped_column(
        ForeignKey("listings.id"),
        nullable=False,
        index=True
    )
    listing: Mapped["Listing"] = relationship("Listing", back_populates="images")

    media_file_id: Mapped[str] = mapped_column(
        ForeignKey("media_files.id"),
        nullable=False,
        index=True
    )
    media_file: Mapped["MediaFile"] = relationship("MediaFile")

    # Информация об изображении
    url: Mapped[str] = mapped_column(String(1000), nullable=False)
    thumbnail_url: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    alt_text: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # Настройки отображения
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    is_primary: Mapped[bool] = mapped_column(default=False, nullable=False, index=True)

    # Метаданные изображения
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)