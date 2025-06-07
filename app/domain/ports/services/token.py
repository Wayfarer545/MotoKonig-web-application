# app/domain/ports/token.py

from datetime import timedelta
from typing import Any, Protocol


class TokenServicePort(Protocol):
    """Порт для работы с токенами"""

    async def create_access_token(
            self,
            data: dict[str, Any],
            expires_delta: timedelta | None = None
    ) -> str:
        """Создать access token"""
        ...

    async def create_refresh_token(
            self,
            data: dict[str, Any],
            expires_delta: timedelta | None = None
    ) -> str:
        """Создать refresh token"""
        ...

    async def decode_token(self, token: str) -> dict[str, Any]:
        """Декодировать токен"""
        ...

    async def blacklist_token(self, token: str, expire_time: int) -> None:
        """Добавить токен в черный список"""
        ...

    async def is_token_blacklisted(self, token: str) -> bool:
        """Проверить, находится ли токен в черном списке"""
        ...
