# app/infrastructure/repositories/sql_media_file_repo.py

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.media_file import MediaFile
from app.domain.ports.media_file_repository import IMediaFileRepository
from app.domain.value_objects.file_type import FileType
from app.infrastructure.models.media_file_model import MediaFile as MediaFileModel


class SqlMediaFileRepository(IMediaFileRepository):
    """SQLAlchemy реализация репозитория медиафайлов"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, media_file: MediaFile) -> MediaFile:
        """Добавить новый медиафайл"""
        db_file = MediaFileModel(
            owner_id=media_file.owner_id,
            file_type=media_file.file_type,
            original_name=media_file.original_name,
            file_key=media_file.file_key,
            bucket=media_file.bucket,
            content_type=media_file.content_type,
            size_bytes=media_file.size_bytes,
            url=media_file.url,
            is_public=media_file.is_public,
        )

        self.session.add(db_file)
        await self.session.flush()
        await self.session.refresh(db_file)

        # Обновляем доменную сущность
        media_file.id = db_file.id
        media_file.created_at = db_file.created_at
        media_file.updated_at = db_file.updated_at

        return media_file

    async def get_by_id(self, file_id: UUID) -> MediaFile | None:
        """Получить медиафайл по ID"""
        result = await self.session.execute(
            select(MediaFileModel).where(MediaFileModel.id == file_id)
        )
        db_file = result.scalar_one_or_none()

        if db_file:
            return self._to_domain_entity(db_file)
        return None

    async def get_by_key(self, file_key: str) -> MediaFile | None:
        """Получить медиафайл по ключу"""
        result = await self.session.execute(
            select(MediaFileModel).where(MediaFileModel.file_key == file_key)
        )
        db_file = result.scalar_one_or_none()

        if db_file:
            return self._to_domain_entity(db_file)
        return None

    async def get_by_owner(self, owner_id: UUID, file_type: FileType | None = None) -> list[MediaFile]:
        """Получить медиафайлы владельца"""
        query = select(MediaFileModel).where(MediaFileModel.owner_id == owner_id)

        if file_type:
            query = query.where(MediaFileModel.file_type == file_type)

        result = await self.session.execute(query)
        files = result.scalars().all()

        return [self._to_domain_entity(f) for f in files]

    async def update(self, media_file: MediaFile) -> MediaFile:
        """Обновить медиафайл"""
        db_file = await self.session.get(MediaFileModel, media_file.id)

        if db_file:
            # Обновляем поля
            db_file.url = media_file.url
            db_file.is_public = media_file.is_public

            await self.session.flush()
            await self.session.refresh(db_file)

            # Обновляем timestamp в доменной сущности
            media_file.updated_at = db_file.updated_at

        return media_file

    async def delete(self, file_id: UUID) -> bool:
        """Удалить медиафайл"""
        db_file = await self.session.get(MediaFileModel, file_id)

        if db_file:
            await self.session.delete(db_file)
            await self.session.flush()
            return True

        return False

    async def delete_by_key(self, file_key: str) -> bool:
        """Удалить медиафайл по ключу"""
        result = await self.session.execute(
            select(MediaFileModel).where(MediaFileModel.file_key == file_key)
        )
        db_file = result.scalar_one_or_none()

        if db_file:
            await self.session.delete(db_file)
            await self.session.flush()
            return True

        return False

    async def check_owner_access(self, file_key: str, owner_id: UUID) -> bool:
        """Проверить права доступа владельца к файлу"""
        result = await self.session.execute(
            select(MediaFileModel).where(
                MediaFileModel.file_key == file_key,
                MediaFileModel.owner_id == owner_id
            )
        )
        return result.scalar_one_or_none() is not None

    def _to_domain_entity(self, db_file: MediaFileModel) -> MediaFile:
        """Преобразовать модель БД в доменную сущность"""
        return MediaFile(
            file_id=db_file.id,
            owner_id=db_file.owner_id,
            file_type=FileType(db_file.file_type.value),
            original_name=db_file.original_name,
            file_key=db_file.file_key,
            bucket=db_file.bucket,
            content_type=db_file.content_type,
            size_bytes=db_file.size_bytes,
            url=db_file.url,
            is_public=db_file.is_public,
            created_at=db_file.created_at,
            updated_at=db_file.updated_at
        )