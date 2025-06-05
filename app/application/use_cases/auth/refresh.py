# app/application/use_cases/auth/refresh.py

from uuid import UUID, uuid4

from app.domain.ports.token_service import TokenServicePort
from app.domain.ports.user_repository import IUserRepository
from app.infrastructure.specifications.user_specs.user_by_id import UserById


class RefreshTokenUseCase:
    """Use case для обновления токенов"""

    def __init__(
            self,
            token_service: TokenServicePort,
            user_repo: IUserRepository
    ):
        self.token_service = token_service
        self.user_repo = user_repo

    async def execute(self, refresh_token: str) -> dict[str, str]:
        """Обновить access token используя refresh token"""
        try:
            # Декодируем refresh token
            payload = await self.token_service.decode_token(refresh_token)

            # Проверяем тип токена
            if payload.get("type") != "refresh":
                raise ValueError("Invalid token type")

            # Проверяем blacklist
            if await self.token_service.is_token_blacklisted(refresh_token):
                raise ValueError("Token is blacklisted")

            # Проверяем, что пользователь всё ещё активен
            user_id = payload.get("sub")
            user = await self.user_repo.get(UserById(UUID(user_id)))

            if not user or not user.is_active:
                raise ValueError("User not found or deactivated")

            # Создаем новые токены
            new_jti = str(uuid4())
            token_data = {
                "sub": str(user.id),
                "username": user.username,
                "role": user.role.name,
                "jti": new_jti
            }

            access_token = await self.token_service.create_access_token(token_data)
            new_refresh_token = await self.token_service.create_refresh_token(token_data)

            # Старый refresh token в blacklist
            await self.token_service.blacklist_token(
                refresh_token,
                payload.get("exp", 0)
            )

            return {
                "access_token": access_token,
                "refresh_token": new_refresh_token,
                "token_type": "bearer"
            }

        except ValueError as ex:
            raise ValueError(f"Token refresh failed: {str(ex)}") from ex
