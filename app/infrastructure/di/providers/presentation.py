# app/infrastructure/di/providers/presentation.py

from dishka import Provider, Scope, provide

from app.application.controllers.auth_controller import AuthController
from app.application.controllers.motorcycle_controller import MotorcycleController
from app.application.controllers.user_controller import UserController
from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.logout import LogoutUseCase
from app.application.use_cases.auth.pin_auth import PinAuthUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.application.use_cases.auth.register import RegisterUseCase
from app.application.use_cases.motorcycle.create_motorcycle import (
    CreateMotorcycleUseCase,
)
from app.application.use_cases.motorcycle.delete_motorcycle import (
    DeleteMotorcycleUseCase,
)
from app.application.use_cases.motorcycle.get_motorcycle import GetMotorcycleUseCase
from app.application.use_cases.motorcycle.list_motorcycles import ListMotorcyclesUseCase
from app.application.use_cases.motorcycle.update_motorcycle import (
    UpdateMotorcycleUseCase,
)
from app.application.use_cases.user.create_user import CreateUserUseCase
from app.application.use_cases.user.delete_user import DeleteUserUseCase
from app.application.use_cases.user.get_user import GetUserUseCase
from app.application.use_cases.user.list_users import ListUsersUseCase
from app.application.use_cases.user.update_user import UpdateUserUseCase


class PresentationProvider(Provider):
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
    def provide_motorcycle_controller(
        self,
        list_uc: ListMotorcyclesUseCase,
        get_uc: GetMotorcycleUseCase,
        create_uc: CreateMotorcycleUseCase,
        update_uc: UpdateMotorcycleUseCase,
        delete_uc: DeleteMotorcycleUseCase,
    ) -> MotorcycleController:
        return MotorcycleController(list_uc, get_uc, create_uc, update_uc, delete_uc)

    @provide(scope=Scope.REQUEST)
    def provide_auth_controller(
        self,
        login_uc: LoginUseCase,
        logout_uc: LogoutUseCase,
        refresh_uc: RefreshTokenUseCase,
        register_uc: RegisterUseCase,
        pin_auth_uc: PinAuthUseCase,
    ) -> AuthController:
        return AuthController(login_uc, logout_uc, refresh_uc, register_uc, pin_auth_uc)
