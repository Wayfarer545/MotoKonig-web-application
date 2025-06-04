# app/application/use_cases/auth/login.py

from typing import Dict, Any
from uuid import uuid4

from app.domain.ports.user_repository import IUserRepository
from app.domain.ports.password_service import PasswordService
from app.domain.ports.token_service import TokenServicePort
from app.adapters.specifications.user_specs.user_by_name import UserByName


class LoginUseCase:
    """Use case для входа пользователя"""

    def __init__(
            self,
            user_repo: IUserRepository,
            pwd_service: PasswordService,
            token_service: TokenServicePort
    ):
        self.user_repo = user_repo
        self.pwd_service = pwd_service
        self.token_service = token_service

    async def execute(self, username: str, password: str) -> Dict[str, str]:
        """
        Аутентифицировать пользователя и вернуть токены

        Returns:
            Dict с access_token и refresh_token
        """
        # Находим пользователя
        user = await self.user_repo.get(UserByName(username))
        if not user:
            raise ValueError("Invalid credentials")

        # Проверяем пароль
        if not await self.pwd_service.verify(password, user.password_hash):
            raise ValueError("Invalid credentials")

        # Проверяем активность
        if not user.is_active:
            raise ValueError("User is deactivated")

        # Создаем payload для токенов
        jti = str(uuid4())  # JWT ID для отзыва токенов
        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role.name,
            "jti": jti
        }

        # Генерируем токены
        access_token = await self.token_service.create_access_token(token_data)
        refresh_token = await self.token_service.create_refresh_token(token_data)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }