# app/infrastructure/di/providers/infrastructure/provider.py

from advanced_alchemy.extensions.fastapi import AdvancedAlchemy
from dishka import Provider, Scope, provide
from fastapi import Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import Config
from app.domain.ports.repositories.club_invitation import (
    IClubInvitationRepository,
)
from app.domain.ports.repositories.club_membership import (
    IClubMembershipRepository,
)
from app.domain.ports.repositories.file_storage import FileStoragePort
from app.domain.ports.repositories.media_file import IMediaFileRepository
from app.domain.ports.repositories.moto_club import IMotoClubRepository
from app.domain.ports.repositories.motorcycle import IMotorcycleRepository
from app.domain.ports.repositories.pin_storage import PinStoragePort
from app.domain.ports.repositories.profile import IProfileRepository
from app.domain.ports.repositories.social_link import ISocialLinkRepository
from app.domain.ports.repositories.user import IUserRepository
from app.domain.ports.services.password import PasswordService
from app.domain.ports.services.token import TokenServicePort
from app.infrastructure.messaging.redis_client import RedisClient
from app.infrastructure.repositories.sql_club_invitation_repo import (
    SqlClubInvitationRepository,
)
from app.infrastructure.repositories.sql_club_membership_repo import (
    SqlClubMembershipRepository,
)
from app.infrastructure.repositories.sql_media_file_repo import SqlMediaFileRepository
from app.infrastructure.repositories.sql_moto_club_repo import SqlMotoClubRepository
from app.infrastructure.repositories.sql_motorcycle_repo import SqlMotorcycleRepository
from app.infrastructure.repositories.sql_profile_repo import SqlProfileRepository
from app.infrastructure.repositories.sql_social_link_repo import SqlSocialLinkRepository
from app.infrastructure.repositories.sql_user_repo import SqlUserRepository
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

    @provide(scope=Scope.REQUEST)
    def provide_moto_club_repo(self, session: AsyncSession) -> IMotoClubRepository:
        return SqlMotoClubRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_club_membership_repo(self, session: AsyncSession) -> IClubMembershipRepository:
        return SqlClubMembershipRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_club_invitation_repo(self, session: AsyncSession) -> IClubInvitationRepository:
        return SqlClubInvitationRepository(session)
