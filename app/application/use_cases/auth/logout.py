# app/application/use_cases/auth/logout.py
from app.domain.ports.token_service import TokenServicePort


class LogoutUseCase:
    """Use case для выхода пользователя"""

    def __init__(self, token_service: TokenServicePort):
        self.token_service = token_service

    async def execute(self, access_token: str) -> None:
        """Добавить токен в blacklist"""
        try:
            payload = await self.token_service.decode_token(access_token)
            expire_time = payload.get("exp", 0)
            await self.token_service.blacklist_token(access_token, expire_time)
        except ValueError:
            # Даже если токен невалидный, добавляем в blacklist
            pass