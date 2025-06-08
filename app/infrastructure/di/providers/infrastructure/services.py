# app/infrastructure/di/providers/infrastructure/services.py

from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from app.config.settings import Config
from app.domain.ports.repositories.file_storage import FileStoragePort
from app.domain.ports.repositories.pin_storage import PinStoragePort
from app.domain.ports.services.password import PasswordService
from app.domain.ports.services.token import TokenServicePort
from app.infrastructure.services.password_service import PasswordServiceImpl
from app.infrastructure.services.pin_storage import RedisPinStorage
from app.infrastructure.services.token_service import JWTTokenService
from app.infrastructure.storage.minio_client import MinIOFileStorage


class ServicesProvider(Provider):
    def __init__(self, config: Config) -> None:
        super().__init__()
        self.config = config

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
