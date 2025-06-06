# app/presentation/schemas/media.py

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict, Field, field_validator

from app.domain.value_objects.file_type import FileType


class BaseModel(_BaseModel):
    """Базовая модель Pydantic с поддержкой атрибутов SQLAlchemy."""
    model_config = ConfigDict(from_attributes=True)


class UploadFileSchema(_BaseModel):
    """Схема для загрузки файла через форму"""
    file_type: FileType = Field(..., description="Тип файла")


class FileUploadResponse(BaseModel):
    """Схема ответа после загрузки файла"""
    id: UUID
    owner_id: UUID
    file_type: str
    original_name: str
    file_key: str
    bucket: str
    content_type: str
    size_bytes: int
    size_mb: float
    url: str
    extension: str
    is_public: bool
    created_at: datetime
    updated_at: datetime


class GetPresignedUrlRequest(_BaseModel):
    """Схема запроса получения presigned URL для скачивания"""
    file_key: str = Field(..., min_length=1, description="Ключ файла в хранилище")
    bucket: str = Field(..., min_length=1, description="Название бакета")
    expiry_seconds: int = Field(3600, ge=1, le=604800, description="Время жизни ссылки в секундах (1 час - 7 дней)")


class GetUploadUrlRequest(_BaseModel):
    """Схема запроса получения presigned URL для загрузки"""
    file_type: FileType = Field(..., description="Тип файла")
    file_name: str = Field(..., min_length=1, max_length=255, description="Имя файла")
    content_type: str = Field(..., min_length=1, description="MIME тип файла")
    expiry_seconds: int = Field(3600, ge=1, le=3600, description="Время жизни ссылки в секундах (максимум 1 час)")

    @field_validator('file_name')
    @classmethod
    def validate_file_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('File name cannot be empty')
        return v.strip()

    @field_validator('content_type')
    @classmethod
    def validate_content_type(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Content type cannot be empty')
        return v.strip()


class PresignedUrlResponse(BaseModel):
    """Схема ответа с presigned URL"""
    download_url: str = Field(..., description="Подписанная ссылка для скачивания")
    expires_in: int = Field(..., description="Время жизни ссылки в секундах")


class UploadUrlResponse(BaseModel):
    """Схема ответа с presigned URL для загрузки"""
    upload_url: str = Field(..., description="Подписанная ссылка для загрузки")
    file_key: str = Field(..., description="Ключ файла в хранилище")
    bucket: str = Field(..., description="Название бакета")
    expires_in: int = Field(..., description="Время жизни ссылки в секундах")


class DeleteFileRequest(_BaseModel):
    """Схема запроса удаления файла"""
    file_key: str = Field(..., min_length=1, description="Ключ файла в хранилище")
    bucket: str = Field(..., min_length=1, description="Название бакета")


class MessageResponse(BaseModel):
    """Схема ответа с сообщением"""
    message: str = Field(..., description="Сообщение о результате операции")


class FileInfoResponse(BaseModel):
    """Схема ответа с информацией о файле"""
    id: UUID
    file_type: str
    original_name: str
    size_mb: float
    content_type: str
    is_public: bool
    created_at: datetime
    # Не показываем file_key, bucket и URL для безопасности