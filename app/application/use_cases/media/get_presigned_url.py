# app/application/use_cases/media/get_presigned_url.py

from uuid import UUID

from app.domain.ports.file_storage import FileStoragePort
from app.domain.ports.media_file_repository import IMediaFileRepository
from app.domain.value_objects.file_type import FileType


class GetPresignedUrlUseCase:
    """Use case для получения подписанных ссылок"""

    def __init__(self, file_storage: FileStoragePort, media_repo: IMediaFileRepository):
        self.file_storage = file_storage
        self.media_repo = media_repo

    async def execute_download_url(
            self,
            file_key: str,
            bucket: str,
            expiry_seconds: int = 3600,
            owner_id: UUID | None = None
    ) -> str:
        """
        Получить подписанную ссылку для скачивания файла

        Args:
            file_key: Ключ файла в хранилище
            bucket: Название бакета
            expiry_seconds: Время жизни ссылки в секундах (по умолчанию 1 час)
            owner_id: ID владельца файла (для дополнительной проверки)

        Returns:
            str: Подписанная ссылка для скачивания

        Raises:
            ValueError: При некорректных параметрах
            RuntimeError: При ошибках генерации ссылки
        """
        # Валидация параметров
        if not file_key or not file_key.strip():
            raise ValueError("File key cannot be empty")

        if not bucket or not bucket.strip():
            raise ValueError("Bucket name cannot be empty")

        if expiry_seconds <= 0 or expiry_seconds > 604800:  # Максимум 7 дней
            raise ValueError("Expiry seconds must be between 1 and 604800 (7 days)")

        # Проверяем права доступа владельца
        if owner_id:
            has_access = await self.media_repo.check_owner_access(file_key.strip(), owner_id)
            if not has_access:
                raise ValueError("File not found or access denied")
        else:
            # Если owner_id не указан, проверяем существование файла в БД
            file_info = await self.media_repo.get_by_key(file_key.strip())
            if not file_info:
                raise ValueError("File not found")

        # Проверяем существование файла в хранилище
        file_exists = await self.file_storage.file_exists(file_key, bucket)
        if not file_exists:
            raise ValueError("File not found in storage")

        try:
            url = await self.file_storage.get_presigned_url(
                file_key=file_key.strip(),
                bucket=bucket.strip(),
                expiry_seconds=expiry_seconds
            )

            return url

        except Exception as e:
            raise RuntimeError(f"Failed to generate presigned URL: {str(e)}") from e

    async def execute_upload_url(
            self,
            file_type: FileType,
            file_name: str,
            content_type: str,
            owner_id: UUID,
            expiry_seconds: int = 3600
    ) -> dict[str, str]:
        """
        Получить подписанную ссылку для загрузки файла

        Args:
            file_type: Тип файла
            file_name: Имя файла
            content_type: MIME тип файла
            owner_id: ID владельца файла
            expiry_seconds: Время жизни ссылки в секундах

        Returns:
            dict: Словарь с url, file_key и bucket

        Raises:
            ValueError: При некорректных параметрах
            RuntimeError: При ошибках генерации ссылки
        """
        # Валидация параметров
        if not file_name or not file_name.strip():
            raise ValueError("File name cannot be empty")

        if not content_type or not content_type.strip():
            raise ValueError("Content type cannot be empty")

        if expiry_seconds <= 0 or expiry_seconds > 3600:  # Максимум 1 час для загрузки
            raise ValueError("Expiry seconds must be between 1 and 3600 (1 hour)")

        # Валидация MIME типа для данного типа файла
        allowed_types = file_type.get_allowed_content_types()
        if content_type not in allowed_types:
            raise ValueError(
                f"Content type {content_type} not allowed for {file_type.value}. "
                f"Allowed types: {', '.join(allowed_types)}"
            )

        try:
            # Генерируем уникальный ключ файла
            import hashlib
            from datetime import datetime
            from uuid import uuid4

            # Временное решение для генерации ключа
            timestamp = datetime.utcnow().strftime("%Y/%m/%d")
            unique_id = str(uuid4())[:8]
            extension = file_name.split('.')[-1].lower() if '.' in file_name else ''
            safe_name = hashlib.md5(file_name.encode()).hexdigest()[:8]

            if extension:
                file_key = f"{timestamp}/{owner_id}/{safe_name}_{unique_id}.{extension}"
            else:
                file_key = f"{timestamp}/{owner_id}/{safe_name}_{unique_id}"

            bucket = file_type.get_bucket_name()

            url = await self.file_storage.get_upload_presigned_url(
                file_key=file_key,
                bucket=bucket,
                content_type=content_type.strip(),
                expiry_seconds=expiry_seconds
            )

            return {
                "upload_url": url,
                "file_key": file_key,
                "bucket": bucket
            }

        except Exception as e:
            raise RuntimeError(f"Failed to generate upload presigned URL: {str(e)}") from e
