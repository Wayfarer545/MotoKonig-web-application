# app/application/use_cases/media/delete_file.py

from uuid import UUID

from app.domain.ports.repositories.file_storage import FileStoragePort

from app.domain.ports.repositories.media_file import IMediaFileRepository


class DeleteFileUseCase:
    """Use case для удаления файлов"""

    def __init__(self, file_storage: FileStoragePort, media_repo: IMediaFileRepository):
        self.file_storage = file_storage
        self.media_repo = media_repo

    async def execute(
            self,
            file_key: str,
            bucket: str,
            owner_id: UUID | None = None
    ) -> bool:
        """
        Удалить файл из хранилища

        Args:
            file_key: Ключ файла в хранилище
            bucket: Название бакета
            owner_id: ID владельца файла (для дополнительной проверки)

        Returns:
            bool: True если файл был удален, False если файл не найден

        Raises:
            ValueError: При некорректных параметрах
            RuntimeError: При ошибках удаления
        """
        # Валидация параметров
        if not file_key or not file_key.strip():
            raise ValueError("File key cannot be empty")

        if not bucket or not bucket.strip():
            raise ValueError("Bucket name cannot be empty")

        # Проверяем права доступа владельца
        if owner_id:
            has_access = await self.media_repo.check_owner_access(file_key.strip(), owner_id)
            if not has_access:
                raise ValueError("File not found or access denied")

        try:
            # Удаляем файл из хранилища
            storage_success = await self.file_storage.delete_file(
                file_key=file_key.strip(),
                bucket=bucket.strip()
            )

            # Удаляем запись из БД
            db_success = await self.media_repo.delete_by_key(file_key.strip())

            return storage_success and db_success

        except Exception as e:
            raise RuntimeError(f"Failed to delete file: {str(e)}") from e
