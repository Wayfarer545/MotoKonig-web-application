# app/application/use_cases/media/upload_file.py

from uuid import UUID

from app.domain.entities.media_file import MediaFile
from app.domain.ports.file_storage import FileStoragePort
from app.domain.ports.media_file_repository import IMediaFileRepository
from app.domain.value_objects.file_type import FileType


class UploadFileUseCase:
    """Use case для загрузки файлов"""

    def __init__(self, file_storage: FileStoragePort, media_repo: IMediaFileRepository):
        self.file_storage = file_storage
        self.media_repo = media_repo

    async def execute(
            self,
            file_content: bytes,
            file_name: str,
            file_type: FileType,
            content_type: str,
            owner_id: UUID
    ) -> MediaFile:
        """
        Загрузить файл в хранилище

        Args:
            file_content: Содержимое файла в байтах
            file_name: Оригинальное имя файла
            file_type: Тип файла (avatar, motorcycle_photo, etc.)
            content_type: MIME тип файла
            owner_id: ID владельца файла

        Returns:
            MediaFile: Созданная сущность медиафайла

        Raises:
            ValueError: При некорректных данных файла
            RuntimeError: При ошибках загрузки
        """
        # Валидация размера файла
        max_size_bytes = file_type.get_max_size_mb() * 1024 * 1024
        if len(file_content) > max_size_bytes:
            raise ValueError(
                f"File size {len(file_content)} bytes exceeds maximum allowed "
                f"{file_type.get_max_size_mb()}MB for {file_type.value}"
            )

        # Валидация MIME типа
        allowed_types = file_type.get_allowed_content_types()
        if content_type not in allowed_types:
            raise ValueError(
                f"Content type {content_type} not allowed for {file_type.value}. "
                f"Allowed types: {', '.join(allowed_types)}"
            )

        # Валидация имени файла
        if not file_name or not file_name.strip():
            raise ValueError("File name cannot be empty")

        # Загружаем файл в хранилище
        try:
            media_file = await self.file_storage.upload_file(
                file_content=file_content,
                file_name=file_name.strip(),
                file_type=file_type,
                content_type=content_type,
                owner_id=owner_id
            )

            # Сохраняем информацию о файле в БД
            saved_file = await self.media_repo.add(media_file)

            return saved_file

        except Exception as e:
            raise RuntimeError(f"Failed to upload file: {str(e)}") from e
