from dishka import Provider, Scope, provide

from app.application.use_cases.user.create_user import CreateUserUseCase
from app.application.use_cases.user.delete_user import DeleteUserUseCase
from app.application.use_cases.user.get_user import GetUserUseCase
from app.application.use_cases.user.list_users import ListUsersUseCase
from app.application.use_cases.user.update_user import UpdateUserUseCase
from app.domain.ports.repositories.user import IUserRepository
from app.domain.ports.services.password import PasswordService


class UserUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_list_users_uc(self, repo: IUserRepository) -> ListUsersUseCase:
        return ListUsersUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_user_uc(self, repo: IUserRepository) -> GetUserUseCase:
        return GetUserUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_create_user_uc(self, repo: IUserRepository, pwd_service: PasswordService) -> CreateUserUseCase:
        return CreateUserUseCase(repo, pwd_service)

    @provide(scope=Scope.REQUEST)
    def provide_update_user_uc(self, repo: IUserRepository, pwd_service: PasswordService) -> UpdateUserUseCase:
        return UpdateUserUseCase(repo, pwd_service)

    @provide(scope=Scope.REQUEST)
    def provide_delete_user_uc(self, repo: IUserRepository) -> DeleteUserUseCase:
        return DeleteUserUseCase(repo)
