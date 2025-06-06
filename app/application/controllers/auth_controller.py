# app/application/controllers/auth_controller.py

from typing import Any
from uuid import UUID

from app.application.exceptions import (
    BadRequestError,
    InternalError,
    TooManyRequestsError,
    UnauthorizedError,
)
from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.logout import LogoutUseCase
from app.application.use_cases.auth.pin_auth import PinAuthUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase
from app.application.use_cases.auth.register import RegisterUseCase


class AuthController:
    """Контроллер для аутентификации"""

    def __init__(
            self,
            login_uc: LoginUseCase,
            logout_uc: LogoutUseCase,
            refresh_uc: RefreshTokenUseCase,
            register_uc: RegisterUseCase,
            pin_auth_uc: PinAuthUseCase
    ):
        self.login_uc = login_uc
        self.logout_uc = logout_uc
        self.refresh_uc = refresh_uc
        self.register_uc = register_uc
        self.pin_auth_uc = pin_auth_uc

    async def login(self, username: str, password: str) -> dict[str, str]:
        """Аутентифицировать пользователя"""
        try:
            return await self.login_uc.execute(username, password)
        except ValueError as ex:
            raise UnauthorizedError(str(ex)) from ex

    async def logout(self, token: str) -> dict[str, str]:
        """Выйти из системы"""
        await self.logout_uc.execute(token)
        return {"message": "Successfully logged out"}

    async def refresh(self, refresh_token: str) -> dict[str, str]:
        """Обновить токены"""
        try:
            return await self.refresh_uc.execute(refresh_token)
        except ValueError as ex:
            raise UnauthorizedError(str(ex)) from ex

    async def register(self, username: str, password: str) -> dict[str, Any]:
        """Зарегистрировать нового пользователя"""
        try:
            user = await self.register_uc.execute(username, password)
            return {
                "id": str(user.id),
                "username": user.username,
                "role": user.role.name,
                "message": "Registration successful",
            }
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def list_devices(self, user_id: UUID) -> list[dict[str, Any]]:
        """Получить список устройств пользователя"""
        try:
            devices = await self.pin_auth_uc.list_devices(user_id)
            return devices
        except Exception as ex:  # pragma: no cover - unexpected
            raise InternalError(f"Failed to retrieve devices: {ex}") from ex

    async def revoke_device(self, user_id: UUID, device_id: str) -> None:
        """Отозвать доступ устройства"""
        try:
            await self.pin_auth_uc.revoke_device(user_id, device_id)
        except Exception as ex:  # pragma: no cover - unexpected
            raise InternalError(f"Failed to revoke device: {ex}") from ex

    async def setup_pin(
        self,
        user_id: UUID,
        pin_code: str,
        device_id: str,
        device_name: str,
    ) -> dict[str, Any]:
        """Установить PIN для устройства"""
        try:
            return await self.pin_auth_uc.setup_pin(
                user_id=user_id,
                pin_code=pin_code,
                device_id=device_id,
                device_name=device_name,
            )
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex



    async def pin_login(
        self,
        pin_code: str,
        device_id: str,
        refresh_token: str,
    ) -> dict[str, str]:
        """Войти по PIN-коду"""
        try:
            result = await self.pin_auth_uc.verify_pin(
                pin_code=pin_code,
                device_id=device_id,
                refresh_token=refresh_token,
            )

            if not result:
                raise UnauthorizedError("Invalid PIN or refresh token")

            return result

        except ValueError as ex:
            raise TooManyRequestsError(str(ex)) from ex
