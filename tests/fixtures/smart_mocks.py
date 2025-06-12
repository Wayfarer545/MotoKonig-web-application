# tests/fixtures/smart_mocks.py
from typing import Dict, Any, List, Set
import time

from app.domain.ports.services.token import TokenServicePort
from app.domain.ports.services.password import PasswordService


class SmartTokenServiceMock(TokenServicePort):
    """Умный мок токен-сервиса с отслеживанием состояния"""

    def __init__(self):
        self.created_tokens: List[tuple[str, Dict[str, Any]]] = []
        self.blacklisted_tokens: Set[str] = set()
        self.token_counter = 0

    async def create_access_token(self, data: Dict[str, Any], expires_delta: int = None) -> str:
        self.token_counter += 1
        token = f"access_token_{self.token_counter}_{data.get('sub', 'unknown')}"
        self.created_tokens.append((token, {**data, "type": "access"}))
        return token

    async def create_refresh_token(self, data: Dict[str, Any], expires_delta: int = None) -> str:
        self.token_counter += 1
        token = f"refresh_token_{self.token_counter}_{data.get('sub', 'unknown')}"
        self.created_tokens.append((token, {**data, "type": "refresh"}))
        return token

    async def decode_token(self, token: str) -> Dict[str, Any]:
        if token in self.blacklisted_tokens:
            raise ValueError("Token is blacklisted")

        # Найти токен в созданных
        for created_token, data in self.created_tokens:
            if created_token == token:
                return {**data, "exp": int(time.time()) + 3600}

        raise ValueError("Invalid token")

    async def blacklist_token(self, token: str, expire_time: int) -> None:
        self.blacklisted_tokens.add(token)

    async def is_token_blacklisted(self, token: str) -> bool:
        return token in self.blacklisted_tokens

    def verify_token_created_for_user(self, user_id: str) -> bool:
        """Проверить, что токен был создан для конкретного пользователя"""
        return any(data.get("sub") == user_id for _, data in self.created_tokens)

    def get_tokens_for_user(self, user_id: str) -> List[str]:
        """Получить все токены для пользователя"""
        return [token for token, data in self.created_tokens if data.get("sub") == user_id]


class SmartPasswordServiceMock(PasswordService):
    """Умный мок пароль-сервиса"""

    def __init__(self):
        self.hash_calls: List[str] = []
        self.verify_calls: List[tuple[str, str]] = []

    async def hash(self, password: str) -> str:
        self.hash_calls.append(password)
        return f"hashed_{password}"

    async def verify(self, password: str, hashed: str) -> bool:
        self.verify_calls.append((password, hashed))
        return hashed == f"hashed_{password}"

    def verify_password_was_hashed(self, password: str) -> bool:
        """Проверить, что пароль был захеширован"""
        return password in self.hash_calls

