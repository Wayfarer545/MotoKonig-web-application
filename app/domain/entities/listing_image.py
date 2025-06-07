# app/domain/entities/listing_image.py

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    pass


class ListingImage:
    """
    Доменная сущность изображения объявления

    Инварианты:
    - URL изображения не может быть пустым
    - Порядок сортировки должен быть неотрицательным
    - Только одно изображение может быть главным для объявления
    """

    def __init__(
            self,
            *,
            image_id: UUID | None = None,
            listing_id: UUID,
            media_file_id: UUID,
            url: str,
            thumbnail_url: str | None = None,
            alt_text: str | None = None,
            sort_order: int = 0,
            is_primary: bool = False,
            width: int | None = None,
            height: int | None = None,
            file_size: int | None = None,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ):
        # Валидация инвариантов
        self._validate_url(url)
        if thumbnail_url is not None:
            self._validate_url(thumbnail_url)
        if alt_text is not None:
            self._validate_alt_text(alt_text)
        self._validate_sort_order(sort_order)
        if width is not None:
            self._validate_dimension(width, "width")
        if height is not None:
            self._validate_dimension(height, "height")
        if file_size is not None:
            self._validate_file_size(file_size)

        self.id: UUID = image_id or uuid4()
        self.listing_id: UUID = listing_id
        self.media_file_id: UUID = media_file_id
        self.url: str = url.strip()
        self.thumbnail_url: str | None = thumbnail_url.strip() if thumbnail_url else None
        self.alt_text: str | None = alt_text.strip() if alt_text else None
        self.sort_order: int = sort_order
        self.is_primary: bool = is_primary
        self.width: int | None = width
        self.height: int | None = height
        self.file_size: int | None = file_size
        self.created_at: datetime | None = created_at
        self.updated_at: datetime | None = updated_at

    def _validate_url(self, url: str) -> None:
        """Валидация URL"""
        if not url or not url.strip():
            raise ValueError("Image URL cannot be empty")
        if len(url.strip()) > 1000:
            raise ValueError("Image URL cannot be longer than 1000 characters")

    def _validate_alt_text(self, alt_text: str) -> None:
        """Валидация альтернативного текста"""
        if len(alt_text.strip()) > 200:
            raise ValueError("Alt text cannot be longer than 200 characters")

    def _validate_sort_order(self, sort_order: int) -> None:
        """Валидация порядка сортировки"""
        if sort_order < 0:
            raise ValueError("Sort order cannot be negative")

    def _validate_dimension(self, dimension: int, dimension_name: str) -> None:
        """Валидация размеров изображения"""
        if dimension <= 0:
            raise ValueError(f"Image {dimension_name} must be positive")
        if dimension > 10000:
            raise ValueError(f"Image {dimension_name} seems too large")

    def _validate_file_size(self, file_size: int) -> None:
        """Валидация размера файла"""
        if file_size <= 0:
            raise ValueError("File size must be positive")
        # Максимум 10MB для изображения
        if file_size > 10 * 1024 * 1024:
            raise ValueError("File size is too large (max 10MB)")

    def set_as_primary(self) -> None:
        """Сделать изображение главным"""
        self.is_primary = True

    def unset_as_primary(self) -> None:
        """Убрать отметку главного изображения"""
        self.is_primary = False

    def update_sort_order(self, sort_order: int) -> None:
        """Обновить порядок сортировки"""
        self._validate_sort_order(sort_order)
        self.sort_order = sort_order

    def update_alt_text(self, alt_text: str | None) -> None:
        """Обновить альтернативный текст"""
        if alt_text is not None:
            self._validate_alt_text(alt_text)
        self.alt_text = alt_text.strip() if alt_text else None

    def update_thumbnail_url(self, thumbnail_url: str | None) -> None:
        """Обновить URL миниатюры"""
        if thumbnail_url is not None:
            self._validate_url(thumbnail_url)
        self.thumbnail_url = thumbnail_url.strip() if thumbnail_url else None

    def get_display_url(self, use_thumbnail: bool = False) -> str:
        """Получить URL для отображения"""
        if use_thumbnail and self.thumbnail_url:
            return self.thumbnail_url
        return self.url

    def get_aspect_ratio(self) -> float | None:
        """Получить соотношение сторон"""
        if self.width and self.height and self.height > 0:
            return self.width / self.height
        return None

    def get_file_size_mb(self) -> float | None:
        """Получить размер файла в MB"""
        if self.file_size:
            return round(self.file_size / (1024 * 1024), 2)
        return None

    def to_dto(self) -> dict:
        """Конвертировать в DTO для API"""
        return {
            "id": self.id,
            "listing_id": self.listing_id,
            "media_file_id": self.media_file_id,
            "url": self.url,
            "thumbnail_url": self.thumbnail_url,
            "alt_text": self.alt_text,
            "sort_order": self.sort_order,
            "is_primary": self.is_primary,
            "width": self.width,
            "height": self.height,
            "file_size": self.file_size,
            "file_size_mb": self.get_file_size_mb(),
            "aspect_ratio": self.get_aspect_ratio(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }