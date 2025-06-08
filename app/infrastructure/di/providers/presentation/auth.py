# app/infrastructure/di/providers/presentation/auth.py

from dishka import Provider, Scope, provide

from app.application.controllers.auth_controller import AuthController
from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.logout import LogoutUseCase
from app.application.use_cases.auth.pin_auth import PinAuthUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.application.use_cases.auth.register import RegisterUseCase


class AuthControllerProvider(Provider):
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
