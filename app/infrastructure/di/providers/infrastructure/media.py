# app/infrastructure/di/providers/infrastructure/media.py

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.repositories.media_file import IMediaFileRepository
from app.infrastructure.repositories.sql_media_file_repo import SqlMediaFileRepository


class MediaRepoProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_media_file_repo(self, session: AsyncSession) -> IMediaFileRepository:
        return SqlMediaFileRepository(session)
