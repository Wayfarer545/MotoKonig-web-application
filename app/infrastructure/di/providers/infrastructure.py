# app/infrastructure/di/providers/infrastructure.py

from advanced_alchemy.extensions.fastapi import AdvancedAlchemy
from dishka import Provider, Scope, provide
from fastapi import Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import Config
from app.domain.ports.motorcycle_repository import IMotorcycleRepository
from app.domain.ports.password_service import PasswordService
from app.domain.ports.pin_storage import PinStoragePort
from app.domain.ports.token_service import TokenServicePort
from app.domain.ports.user_repository import IUserRepository
from app.domain.ports.profile_repository import IProfileRepository
from app.domain.ports.social_link_repository import ISocialLinkRepository
from app.domain.ports.media_file_repository import IMediaFileRepository
from app.domain.ports.file_storage import FileStoragePort
from app.infrastructure.messaging.redis_client import RedisClient
from app.infrastructure.repositories.sql_motorcycle_repo import SqlMotorcycleRepository
from app.infrastructure.repositories.sql_user_repo import SqlUserRepository
from app.infrastructure.repositories.sql_profile_repo import SqlProfileRepository
from app.infrastructure.repositories.sql_social_link_repo import SqlSocialLinkRepository
from app.infrastructure.repositories.sql_media_file_repo import SqlMediaFileRepository
from app.infrastructure.services.password_service import PasswordServiceImpl
from app.infrastructure.services.pin_storage import RedisPinStorage
from app.infrastructure.services.token_service import JWTTokenService
from app.infrastructure.storage.minio_client import MinIOFileStorage


class InfrastructureProvider(Provider):
    def __init__(self, alchemy: AdvancedAlchemy, config: Config):
        super().__init__()
        self.alchemy = alchemy
        self.config = config

    @provide(scope=Scope.REQUEST)
    def provide_db_session(self, request: Request) -> AsyncSession:
        """Get DB session from Advanced-Alchemy."""
        return self.alchemy.get_session(request)

    @provide(scope=Scope.APP)
    async def provide_redis(self) -> Redis:
        """Provide Redis client."""
        await RedisClient.create_pool(self.config.redis)
        return await RedisClient.get_client()

    # Repositories
    @provide(scope=Scope.REQUEST)
    def provide_user_repo(self, session: AsyncSession) -> IUserRepository:
        return SqlUserRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_motorcycle_repo(self, session: AsyncSession) -> IMotorcycleRepository:
        return SqlMotorcycleRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_profile_repo(self, session: AsyncSession) -> IProfileRepository:
        return SqlProfileRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_social_link_repo(self, session: AsyncSession) -> ISocialLinkRepository:
        return SqlSocialLinkRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_media_file_repo(self, session: AsyncSession) -> IMediaFileRepository:
        return SqlMediaFileRepository(session)

    # Services
    @provide(scope=Scope.APP)
    def provide_password_service(self) -> PasswordService:
        return PasswordServiceImpl()

    @provide(scope=Scope.APP)
    def provide_token_service(self, redis: Redis) -> TokenServicePort:
        return JWTTokenService(redis, self.config.security)

    @provide(scope=Scope.APP)
    def provide_pin_storage(self, redis: Redis) -> PinStoragePort:
        return RedisPinStorage(redis)

    @provide(scope=Scope.APP)
    def provide_file_storage(self) -> FileStoragePort:
        return MinIOFileStorage(self.config.minio)