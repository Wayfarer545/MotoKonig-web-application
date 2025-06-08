# app/infrastructure/di/providers/use_cases/auth.py

from dishka import Provider, Scope, provide

from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.logout import LogoutUseCase
from app.application.use_cases.auth.pin_auth import PinAuthUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.application.use_cases.auth.register import RegisterUseCase
from app.domain.ports.repositories.pin_storage import PinStoragePort
from app.domain.ports.repositories.user import IUserRepository
from app.domain.ports.services.password import PasswordService
from app.domain.ports.services.token import TokenServicePort


class AuthUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_login_uc(
        self,
        repo: IUserRepository,
        pwd_service: PasswordService,
        token_service: TokenServicePort,
    ) -> LoginUseCase:
        return LoginUseCase(repo, pwd_service, token_service)

    @provide(scope=Scope.REQUEST)
    def provide_logout_uc(self, token_service: TokenServicePort) -> LogoutUseCase:
        return LogoutUseCase(token_service)

    @provide(scope=Scope.REQUEST)
    def provide_refresh_uc(
        self,
        token_service: TokenServicePort,
        repo: IUserRepository,
    ) -> RefreshTokenUseCase:
        return RefreshTokenUseCase(token_service, repo)

    @provide(scope=Scope.REQUEST)
    def provide_register_uc(
        self,
        repo: IUserRepository,
        pwd_service: PasswordService,
    ) -> RegisterUseCase:
        return RegisterUseCase(repo, pwd_service)

    @provide(scope=Scope.REQUEST)
    def provide_pin_auth_uc(
        self,
        user_repo: IUserRepository,
        token_service: TokenServicePort,
        pin_storage: PinStoragePort,
    ) -> PinAuthUseCase:
        return PinAuthUseCase(user_repo, token_service, pin_storage)
