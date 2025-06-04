# app/infrastructure/di/container.py

from advanced_alchemy.extensions.fastapi import AdvancedAlchemy
from application.use_cases.auth.pin_auth import PinAuthUseCase
from application.use_cases.auth.register import RegisterUseCase
from dishka import Provider, Scope, provide
from domain.ports.pin_storage import PinStoragePort
from fastapi import Request
from infrastructure.services.pin_storage import RedisPinStorage
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

# Repositories
from app.adapters.repositories.sql_user_repo import SqlUserRepository
from app.application.controllers.auth_controller import AuthController

# Controllers
from app.application.controllers.user_controller import UserController

# Use Cases - Auth
from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.logout import LogoutUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.application.use_cases.user.create_user import CreateUserUseCase
from app.application.use_cases.user.delete_user import DeleteUserUseCase
from app.application.use_cases.user.get_user import GetUserUseCase

# Use Cases - User
from app.application.use_cases.user.list_users import ListUsersUseCase
from app.application.use_cases.user.update_user import UpdateUserUseCase
from app.config.settings import Config

# Services
from app.domain.ports.password_service import PasswordService
from app.domain.ports.token_service import TokenServicePort
from app.domain.ports.user_repository import IUserRepository
from app.infrastructure.messaging.redis_client import RedisClient
from app.infrastructure.services.password_service import PasswordServiceImpl
from app.infrastructure.services.token_service import JWTTokenService


class ApplicationProvider(Provider):
    def __init__(self, alchemy: AdvancedAlchemy, config: Config):
        super().__init__()
        self.alchemy = alchemy
        self.config = config

    @provide(scope=Scope.REQUEST)
    def provide_db_session(self, request: Request) -> AsyncSession:
        """Берём сессию из Advanced-Alchemy"""
        return self.alchemy.get_session(request)

    @provide(scope=Scope.APP)
    async def provide_redis(self) -> Redis:
        """Предоставляем Redis клиент"""
        await RedisClient.create_pool(self.config.redis)
        return await RedisClient.get_client()

    # Repositories
    @provide(scope=Scope.REQUEST)
    def provide_user_repo(self, session: AsyncSession) -> IUserRepository:
        return SqlUserRepository(session)

    # Services
    @provide(scope=Scope.APP)
    def provide_password_service(self) -> PasswordService:
        return PasswordServiceImpl()

    @provide(scope=Scope.APP)
    def provide_token_service(self, redis: Redis) -> TokenServicePort:
        return JWTTokenService(redis, self.config.security)

    # User Use Cases
    @provide(scope=Scope.REQUEST)
    def provide_list_users_uc(self, repo: IUserRepository) -> ListUsersUseCase:
        return ListUsersUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_user_uc(self, repo: IUserRepository) -> GetUserUseCase:
        return GetUserUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_create_user_uc(
            self,
            repo: IUserRepository,
            pwd_service: PasswordService,
    ) -> CreateUserUseCase:
        return CreateUserUseCase(repo, pwd_service)

    @provide(scope=Scope.REQUEST)
    def provide_update_user_uc(
            self,
            repo: IUserRepository,
            pwd_service: PasswordService,
    ) -> UpdateUserUseCase:
        return UpdateUserUseCase(repo, pwd_service)

    @provide(scope=Scope.REQUEST)
    def provide_delete_user_uc(self, repo: IUserRepository) -> DeleteUserUseCase:
        return DeleteUserUseCase(repo)

    # Auth Use Cases
    @provide(scope=Scope.REQUEST)
    def provide_login_uc(
            self,
            repo: IUserRepository,
            pwd_service: PasswordService,
            token_service: TokenServicePort
    ) -> LoginUseCase:
        return LoginUseCase(repo, pwd_service, token_service)

    @provide(scope=Scope.REQUEST)
    def provide_logout_uc(self, token_service: TokenServicePort) -> LogoutUseCase:
        return LogoutUseCase(token_service)

    @provide(scope=Scope.REQUEST)
    def provide_refresh_uc(
            self,
            token_service: TokenServicePort,
            repo: IUserRepository
    ) -> RefreshTokenUseCase:
        return RefreshTokenUseCase(token_service, repo)

    # Controllers
    @provide(scope=Scope.REQUEST)
    def provide_user_controller(
            self,
            list_uc: ListUsersUseCase,
            get_uc: GetUserUseCase,
            create_uc: CreateUserUseCase,
            update_uc: UpdateUserUseCase,
            delete_uc: DeleteUserUseCase,
    ) -> UserController:
        return UserController(list_uc, get_uc, create_uc, update_uc, delete_uc)

    @provide(scope=Scope.REQUEST)
    def provide_register_uc(
            self,
            repo: IUserRepository,
            pwd_service: PasswordService
    ) -> RegisterUseCase:
        return RegisterUseCase(repo, pwd_service)

    @provide(scope=Scope.APP)
    def provide_pin_storage(self, redis: Redis) -> PinStoragePort:
        return RedisPinStorage(redis)

    @provide(scope=Scope.REQUEST)
    def provide_pin_auth_uc(
            self,
            user_repo: IUserRepository,
            token_service: TokenServicePort,
            pin_storage: PinStoragePort
    ) -> PinAuthUseCase:
        return PinAuthUseCase(user_repo, token_service, pin_storage)

    # Обновляем провайдер AuthController:
    @provide(scope=Scope.REQUEST)
    def provide_auth_controller(
            self,
            login_uc: LoginUseCase,
            logout_uc: LogoutUseCase,
            refresh_uc: RefreshTokenUseCase,
            register_uc: RegisterUseCase,
            pin_auth_uc: PinAuthUseCase  # Добавляем
    ) -> AuthController:
        return AuthController(
            login_uc, logout_uc, refresh_uc, register_uc, pin_auth_uc
        )
