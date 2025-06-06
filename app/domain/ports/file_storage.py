# app/domain/ports/file_storage.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.media_file import MediaFile
from app.domain.value_objects.file_type import FileType


class FileStoragePort(Protocol):
    """Порт для работы с файловым хранилищем"""

    async def upload_file(
            self,
            file_content: bytes,
            file_name: str,
            file_type: FileType,
            content_type: str,
            owner_id: UUID
    ) -> MediaFile:
        """Загрузить файл в хранилище"""
        ...

    async def delete_file(self, file_key: str, bucket: str) -> bool:
        """Удалить файл из хранилища"""
        ...

    async def get_presigned_url(
            self,
            file_key: str,
            bucket: str,
            expiry_seconds: int = 3600
    ) -> str:
        """Получить подписанную ссылку для доступа к файлу"""
        ...

    async def get_upload_presigned_url(
            self,
            file_key: str,
            bucket: str,
            content_type: str,
            expiry_seconds: int = 3600
    ) -> str:
        """Получить подписанную ссылку для загрузки файла"""
        ...

    async def file_exists(self, file_key: str, bucket: str) -> bool:
        """Проверить существование файла"""
        ...

    async def get_file_info(self, file_key: str, bucket: str) -> dict:
        """Получить метаданные файла"""
        ...