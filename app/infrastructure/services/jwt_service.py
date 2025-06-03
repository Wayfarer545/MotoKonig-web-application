# app/infrastructure/services/jwt_service.py

import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from uuid import uuid4

from app.domain.ports.token_service import TokenService
from app.config.settings import SecuritySettings


class JWTService(TokenService):
    def __init__(self, settings: SecuritySettings, redis_client):
        self.settings = settings
        self.redis = redis_client
        self.access_token_expire = timedelta(minutes=30)
        self.refresh_token_expire = timedelta(days=7)

    async def create_access_token(self, user_id: str, additional_claims: Optional[Dict[str, Any]] = None) -> str:
        claims = {
            "sub": user_id,
            "type": "access",
            "exp": datetime.now(timezone.utc) + self.access_token_expire,
            "iat": datetime.now(timezone.utc),
            "jti": str(uuid4())  # JWT ID для возможности отзыва
        }

        if additional_claims:
            claims.update(additional_claims)

        return jwt.encode(claims, self.settings.secret_key, algorithm=self.settings.algorithm)

    async def create_refresh_token(self, user_id: str) -> str:
        claims = {
            "sub": user_id,
            "type": "refresh",
            "exp": datetime.now(timezone.utc) + self.refresh_token_expire,
            "iat": datetime.now(timezone.utc),
            "jti": str(uuid4())
        }

        return jwt.encode(claims, self.settings.secret_key, algorithm=self.settings.algorithm)

    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        try:
            payload = jwt.decode(
                token,
                self.settings.secret_key,
                algorithms=[self.settings.algorithm]
            )

            # Проверяем, не в блэклисте ли токен
            if await self.is_token_revoked(payload.get("jti")):
                return None

            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    async def revoke_token(self, token: str) -> None:
        """Добавляет токен в блэклист Redis"""
        try:
            payload = jwt.decode(
                token,
                self.settings.secret_key,
                algorithms=[self.settings.algorithm],
                options={"verify_exp": False}  # Позволяем отозвать даже истёкший токен
            )

            jti = payload.get("jti")
            exp = payload.get("exp")

            if jti and exp:
                # Вычисляем TTL для Redis - токен будет в блэклисте до истечения срока
                ttl = exp - datetime.now(timezone.utc).timestamp()
                if ttl > 0:
                    await self.redis.setex(f"blacklist:{jti}", int(ttl), "1")
        except jwt.InvalidTokenError:
            pass  # Невалидный токен - игнорируем

    async def is_token_revoked(self, jti: str) -> bool:
        """Проверяет, находится ли токен в блэклисте"""
        if not jti:
            return False
        return await self.redis.exists(f"blacklist:{jti}") > 0