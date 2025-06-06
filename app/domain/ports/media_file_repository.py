# app/domain/ports/media_file_repository.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.media_file import MediaFile
from app.domain.value_objects.file_type import FileType


class IMediaFileRepository(Protocol):
    """Порт репозитория медиафайлов"""

    async def add(self, media_file: MediaFile) -> MediaFile:
        """Добавить новый медиафайл"""
        ...

    async def get_by_id(self, file_id: UUID) -> MediaFile | None:
        """Получить медиафайл по ID"""
        ...

    async def get_by_key(self, file_key: str) -> MediaFile | None:
        """Получить медиафайл по ключу"""
        ...

    async def get_by_owner(self, owner_id: UUID, file_type: FileType | None = None) -> list[MediaFile]:
        """Получить медиафайлы владельца"""
        ...

    async def update(self, media_file: MediaFile) -> MediaFile:
        """Обновить медиафайл"""
        ...

    async def delete(self, file_id: UUID) -> bool:
        """Удалить медиафайл"""
        ...

    async def delete_by_key(self, file_key: str) -> bool:
        """Удалить медиафайл по ключу"""
        ...

    async def check_owner_access(self, file_key: str, owner_id: UUID) -> bool:
        """Проверить права доступа владельца к файлу"""
        ...