# app/infrastructure/storage/minio_client.py

import hashlib
from datetime import datetime
from uuid import UUID, uuid4

import aioboto3
from botocore.exceptions import ClientError
from domain.ports.repositories.file_storage import FileStoragePort

from app.config.settings import MinIOConfig
from app.domain.entities.media_file import MediaFile
from app.domain.value_objects.file_type import FileType


class MinIOFileStorage(FileStoragePort):
    """MinIO реализация файлового хранилища"""

    def __init__(self, config: MinIOConfig):
        self.config = config
        self.session = aioboto3.Session()

    def _get_client(self):
        """Получить S3 клиент"""
        return self.session.client(
            's3',
            endpoint_url=f"{'https' if self.config.secure else 'http'}://{self.config.endpoint}",
            aws_access_key_id=self.config.access_key,
            aws_secret_access_key=self.config.secret_key,
            region_name=self.config.region,
        )

    def _generate_file_key(self, owner_id: UUID, file_type: FileType, original_name: str) -> str:
        """Генерировать уникальный ключ файла"""
        # Используем timestamp + uuid для уникальности
        timestamp = datetime.utcnow().strftime("%Y/%m/%d")
        unique_id = str(uuid4())[:8]

        # Получаем расширение файла
        extension = original_name.split('.')[-1].lower() if '.' in original_name else ''

        # Создаем безопасное имя файла
        safe_name = hashlib.md5(original_name.encode()).hexdigest()[:8]

        if extension:
            return f"{timestamp}/{owner_id}/{safe_name}_{unique_id}.{extension}"
        else:
            return f"{timestamp}/{owner_id}/{safe_name}_{unique_id}"

    async def _ensure_bucket_exists(self, bucket_name: str) -> None:
        """Убедиться, что бакет существует"""
        async with self._get_client() as s3:
            try:
                await s3.head_bucket(Bucket=bucket_name)
            except ClientError:
                # Бакет не существует, создаем его
                try:
                    await s3.create_bucket(Bucket=bucket_name)
                except ClientError as e:
                    if e.response['Error']['Code'] != 'BucketAlreadyExists':
                        raise

    async def upload_file(
            self,
            file_content: bytes,
            file_name: str,
            file_type: FileType,
            content_type: str,
            owner_id: UUID
    ) -> MediaFile:
        """Загрузить файл в MinIO"""
        bucket = file_type.get_bucket_name()
        file_key = self._generate_file_key(owner_id, file_type, file_name)

        # Убеждаемся, что бакет существует
        await self._ensure_bucket_exists(bucket)

        async with self._get_client() as s3:
            try:
                # Загружаем файл
                await s3.put_object(
                    Bucket=bucket,
                    Key=file_key,
                    Body=file_content,
                    ContentType=content_type,
                    Metadata={
                        'original_name': file_name,
                        'owner_id': str(owner_id),
                        'file_type': file_type.value,
                        'upload_time': datetime.utcnow().isoformat()
                    }
                )

                # Формируем URL
                url = f"{'https' if self.config.secure else 'http'}://{self.config.endpoint}/{bucket}/{file_key}"

                # Создаем доменную сущность
                media_file = MediaFile(
                    owner_id=owner_id,
                    file_type=file_type,
                    original_name=file_name,
                    file_key=file_key,
                    bucket=bucket,
                    content_type=content_type,
                    size_bytes=len(file_content),
                    url=url,
                    is_public=False,
                    created_at=datetime.utcnow()
                )

                return media_file

            except ClientError as e:
                raise RuntimeError(f"Failed to upload file: {e}") from e

    async def delete_file(self, file_key: str, bucket: str) -> bool:
        """Удалить файл из MinIO"""
        async with self._get_client() as s3:
            try:
                await s3.delete_object(Bucket=bucket, Key=file_key)
                return True
            except ClientError:
                return False

    async def get_presigned_url(
            self,
            file_key: str,
            bucket: str,
            expiry_seconds: int = 3600
    ) -> str:
        """Получить подписанную ссылку для скачивания"""
        async with self._get_client() as s3:
            try:
                url = await s3.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': bucket, 'Key': file_key},
                    ExpiresIn=expiry_seconds
                )
                return url
            except ClientError as e:
                raise RuntimeError(f"Failed to generate presigned URL: {e}") from e

    async def get_upload_presigned_url(
            self,
            file_key: str,
            bucket: str,
            content_type: str,
            expiry_seconds: int = 3600
    ) -> str:
        """Получить подписанную ссылку для загрузки"""
        async with self._get_client() as s3:
            try:
                # Убеждаемся, что бакет существует
                await self._ensure_bucket_exists(bucket)

                url = await s3.generate_presigned_url(
                    'put_object',
                    Params={
                        'Bucket': bucket,
                        'Key': file_key,
                        'ContentType': content_type
                    },
                    ExpiresIn=expiry_seconds
                )
                return url
            except ClientError as e:
                raise RuntimeError(f"Failed to generate upload presigned URL: {e}") from e

    async def file_exists(self, file_key: str, bucket: str) -> bool:
        """Проверить существование файла"""
        async with self._get_client() as s3:
            try:
                await s3.head_object(Bucket=bucket, Key=file_key)
                return True
            except ClientError:
                return False

    async def get_file_info(self, file_key: str, bucket: str) -> dict:
        """Получить метаданные файла"""
        async with self._get_client() as s3:
            try:
                response = await s3.head_object(Bucket=bucket, Key=file_key)
                return {
                    'size': response['ContentLength'],
                    'content_type': response['ContentType'],
                    'last_modified': response['LastModified'],
                    'metadata': response.get('Metadata', {})
                }
            except ClientError as e:
                raise RuntimeError(f"Failed to get file info: {e}") from e
