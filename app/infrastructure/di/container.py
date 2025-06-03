# app/infrastructure/di/container.py

from dishka import Provider, provide, Scope
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from advanced_alchemy.extensions.fastapi import AdvancedAlchemy

from app.adapters.repositories.sql_user_repo import SqlUserRepository
from app.domain.ports.user_repository import IUserRepository
from app.domain.ports.password_service import PasswordService
from app.infrastructure.services.password_service import PasswordServiceImpl
from app.infrastructure.adapters.redis.client import create_redis_client

from app.application.use_cases.user.list_users import ListUsersUseCase
from app.application.use_cases.user.get_user import GetUserUseCase
from app.application.use_cases.user.create_user import CreateUserUseCase
from app.application.use_cases.user.update_user import UpdateUserUseCase
from app.application.use_cases.user.delete_user import DeleteUserUseCase
from app.application.controllers.user_controller import UserController


class ApplicationProvider(Provider):
    def __init__(self, alchemy: AdvancedAlchemy):
        super().__init__()
        self.alchemy = alchemy

    @provide(scope=Scope.REQUEST)
    def provide_db_session(self, request: Request) -> AsyncSession:
        """
        Берём сессию из Advanced-Alchemy и напрямую возвращаем AsyncSession.
        Метод get_session возвращает уже готовый AsyncSession — нет нужды await’ить. :contentReference[oaicite:0]{index=0}
        """
        return self.alchemy.get_session(request)

    @provide(scope=Scope.REQUEST)
    def provide_user_repo(self, session: AsyncSession) -> IUserRepository:
        return SqlUserRepository(session)

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
    def provide_password_service(self) -> PasswordService:
        return PasswordServiceImpl()
