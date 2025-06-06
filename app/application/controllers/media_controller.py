# app/application/controllers/media_controller.py

from uuid import UUID

from app.application.exceptions import BadRequestError, NotFoundError
from app.application.use_cases.media.delete_file import DeleteFileUseCase
from app.application.use_cases.media.get_presigned_url import GetPresignedUrlUseCase
from app.application.use_cases.media.upload_file import UploadFileUseCase
from app.domain.value_objects.file_type import FileType


class MediaController:
    """Контроллер для управления медиафайлами"""

    def __init__(
            self,
            upload_uc: UploadFileUseCase,
            delete_uc: DeleteFileUseCase,
            presigned_url_uc: GetPresignedUrlUseCase,
    ):
        self.upload_uc = upload_uc
        self.delete_uc = delete_uc
        self.presigned_url_uc = presigned_url_uc

    async def upload_file(
            self,
            file_content: bytes,
            file_name: str,
            file_type: FileType,
            content_type: str,
            owner_id: UUID
    ) -> dict:
        """Загрузить файл"""
        try:
            media_file = await self.upload_uc.execute(
                file_content=file_content,
                file_name=file_name,
                file_type=file_type,
                content_type=content_type,
                owner_id=owner_id
            )
            return media_file.to_dto()
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def delete_file(
            self,
            file_key: str,
            bucket: str,
            owner_id: UUID | None = None
    ) -> None:
        """Удалить файл"""
        try:
            success = await self.delete_uc.execute(
                file_key=file_key,
                bucket=bucket,
                owner_id=owner_id
            )
            if not success:
                raise NotFoundError("File not found")
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def get_download_url(
            self,
            file_key: str,
            bucket: str,
            expiry_seconds: int = 3600,
            owner_id: UUID | None = None
    ) -> dict[str, str]:
        """Получить ссылку для скачивания"""
        try:
            url = await self.presigned_url_uc.execute_download_url(
                file_key=file_key,
                bucket=bucket,
                expiry_seconds=expiry_seconds,
                owner_id=owner_id
            )
            return {"download_url": url, "expires_in": expiry_seconds}
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def get_upload_url(
            self,
            file_type: FileType,
            file_name: str,
            content_type: str,
            owner_id: UUID,
            expiry_seconds: int = 3600
    ) -> dict[str, str]:
        """Получить ссылку для загрузки"""
        try:
            result = await self.presigned_url_uc.execute_upload_url(
                file_type=file_type,
                file_name=file_name,
                content_type=content_type,
                owner_id=owner_id,
                expiry_seconds=expiry_seconds
            )
            result["expires_in"] = expiry_seconds
            return result
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex
