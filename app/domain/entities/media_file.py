# app/domain/entities/media_file.py

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.domain.value_objects.file_type import FileType

if TYPE_CHECKING:
    pass


class MediaFile:
    """
    Доменная сущность медиафайла

    Инварианты:
    - Размер файла не может быть отрицательным
    - MIME тип должен соответствовать типу файла
    - Имя файла не может быть пустым
    """

    def __init__(
            self,
            *,
            file_id: UUID | None = None,
            owner_id: UUID,
            file_type: FileType,
            original_name: str,
            file_key: str,
            bucket: str,
            content_type: str,
            size_bytes: int,
            url: str,
            is_public: bool = False,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ):
        # Валидация инвариантов
        self._validate_file_name(original_name)
        self._validate_size(size_bytes)
        self._validate_file_size_for_type(file_type, size_bytes)
        self._validate_content_type(file_type, content_type)

        self.id: UUID = file_id or uuid4()
        self.owner_id: UUID = owner_id
        self.file_type: FileType = file_type
        self.original_name: str = original_name.strip()
        self.file_key: str = file_key
        self.bucket: str = bucket
        self.content_type: str = content_type
        self.size_bytes: int = size_bytes
        self.url: str = url
        self.is_public: bool = is_public
        self.created_at: datetime | None = created_at
        self.updated_at: datetime | None = updated_at

    def _validate_file_name(self, name: str) -> None:
        """Валидация имени файла"""
        if not name or not name.strip():
            raise ValueError("File name cannot be empty")
        if len(name.strip()) > 255:
            raise ValueError("File name cannot be longer than 255 characters")

    def _validate_size(self, size: int) -> None:
        """Валидация размера файла"""
        if size < 0:
            raise ValueError("File size cannot be negative")
        # Валидация по типу файла будет в другом методе

    def _validate_content_type(self, file_type: FileType, content_type: str) -> None:
        """Валидация MIME типа"""
        allowed_types = file_type.get_allowed_content_types()
        if content_type not in allowed_types:
            raise ValueError(f"Content type {content_type} not allowed for {file_type.value}")

    def _validate_file_size_for_type(self, file_type: FileType, size: int) -> None:
        """Валидация размера файла для конкретного типа"""
        max_size_bytes = file_type.get_max_size_mb() * 1024 * 1024
        if size > max_size_bytes:
            raise ValueError(f"File size exceeds maximum allowed size of {file_type.get_max_size_mb()}MB")

    def get_size_mb(self) -> float:
        """Получить размер файла в MB"""
        return round(self.size_bytes / (1024 * 1024), 2)

    def get_extension(self) -> str:
        """Получить расширение файла"""
        return self.original_name.split('.')[-1].lower() if '.' in self.original_name else ''

    def make_public(self) -> None:
        """Сделать файл публичным"""
        self.is_public = True

    def make_private(self) -> None:
        """Сделать файл приватным"""
        self.is_public = False

    def update_url(self, new_url: str) -> None:
        """Обновить URL файла"""
        self.url = new_url

    def to_dto(self) -> dict:
        """Конвертировать в DTO для API"""
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "file_type": self.file_type.value,
            "original_name": self.original_name,
            "file_key": self.file_key,
            "bucket": self.bucket,
            "content_type": self.content_type,
            "size_bytes": self.size_bytes,
            "size_mb": self.get_size_mb(),
            "url": self.url,
            "extension": self.get_extension(),
            "is_public": self.is_public,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
