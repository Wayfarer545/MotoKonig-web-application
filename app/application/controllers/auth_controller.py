# app/application/controllers/auth_controller.py

from typing import Dict
from fastapi import HTTPException, status

from app.application.use_cases.auth.login import LoginUseCase
from app.application.use_cases.auth.logout import LogoutUseCase
from app.application.use_cases.auth.refresh import RefreshTokenUseCase


class AuthController:
    """Контроллер для аутентификации"""

    def __init__(
            self,
            login_uc: LoginUseCase,
            logout_uc: LogoutUseCase,
            refresh_uc: RefreshTokenUseCase
    ):
        self.login_uc = login_uc
        self.logout_uc = logout_uc
        self.refresh_uc = refresh_uc

    async def login(self, username: str, password: str) -> Dict[str, str]:
        """Аутентифицировать пользователя"""
        try:
            return await self.login_uc.execute(username, password)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"}
            )

    async def logout(self, token: str) -> Dict[str, str]:
        """Выйти из системы"""
        await self.logout_uc.execute(token)
        return {"message": "Successfully logged out"}

    async def refresh(self, refresh_token: str) -> Dict[str, str]:
        """Обновить токены"""
        try:
            return await self.refresh_uc.execute(refresh_token)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"}
            )