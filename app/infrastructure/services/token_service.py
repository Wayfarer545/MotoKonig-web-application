# app/infrastructure/services/token.py

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from redis.asyncio import Redis

from app.config.settings import SecuritySettings
from app.domain.ports.services.token import TokenServicePort


class JWTTokenService(TokenServicePort):
    """Реализация сервиса для работы с JWT токенами"""

    def __init__(self, redis_client: Redis, security_settings: SecuritySettings):
        self.redis = redis_client
        self.secret_key = security_settings.secret_key
        self.algorithm = security_settings.algorithm
        self.access_token_expire = timedelta(minutes=30)
        self.refresh_token_expire = timedelta(days=7)

    async def create_access_token(
            self,
            data: dict[str, Any],
            expires_delta: timedelta | None = None
    ) -> str:
        """Создать JWT access token"""
        to_encode = data.copy()
        expire = datetime.now(UTC) + (expires_delta or self.access_token_expire)

        to_encode.update({
            "exp": expire,
            "type": "access",
            "iat": datetime.now(UTC)
        })

        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def create_refresh_token(
            self,
            data: dict[str, Any],
            expires_delta: timedelta | None = None
    ) -> str:
        """Создать JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.now(UTC) + (expires_delta or self.refresh_token_expire)

        to_encode.update({
            "exp": expire,
            "type": "refresh",
            "iat": datetime.now(UTC)
        })

        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    async def decode_token(self, token: str) -> dict[str, Any]:
        """Декодировать и валидировать токен"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError as e:
            raise ValueError("Token has expired") from e
        except jwt.InvalidTokenError as e:
            raise ValueError("Invalid token") from e

    async def blacklist_token(self, token: str, expire_time: int) -> None:
        """Добавить токен в Redis blacklist"""
        # Используем jti (JWT ID) если есть, иначе сам токен
        try:
            payload = await self.decode_token(token)
            key = f"blacklist:{payload.get('jti', token)}"
            ttl = expire_time - int(datetime.now(UTC).timestamp())
            if ttl > 0:
                await self.redis.setex(key, ttl, "1")
        except ValueError:
            # Если токен невалидный, всё равно добавляем в blacklist
            key = f"blacklist:{token}"
            await self.redis.setex(key, 3600, "1")  # На час

    async def is_token_blacklisted(self, token: str) -> bool:
        """Проверить наличие токена в blacklist"""
        try:
            payload = await self.decode_token(token)
            key = f"blacklist:{payload.get('jti', token)}"
            return (await self.redis.exists(key)) > 0
        except ValueError:
            return True  # Невалидные токены считаем заблокированными
