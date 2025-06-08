# app/infrastructure/di/providers/presentation/user.py

from dishka import Provider, Scope, provide

from app.application.controllers.user_controller import UserController
from app.application.use_cases.user.create_user import CreateUserUseCase
from app.application.use_cases.user.delete_user import DeleteUserUseCase
from app.application.use_cases.user.get_user import GetUserUseCase
from app.application.use_cases.user.list_users import ListUsersUseCase
from app.application.use_cases.user.update_user import UpdateUserUseCase


class UserControllerProvider(Provider):
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
