# app/application/use_cases/auth/pin_auth.py

import hashlib
import hmac
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID, uuid4

from app.domain.ports.pin_storage import PinStoragePort
from app.domain.ports.token_service import TokenServicePort
from app.domain.ports.user_repository import IUserRepository
from app.infrastructure.specs.user.user_by_id import UserById


class PinAuthUseCase:
    """PIN-аутентификация для мобильных приложений"""

    MAX_ATTEMPTS = 5
    PIN_TTL = timedelta(days=30)

    def __init__(
            self,
            user_repo: IUserRepository,
            token_service: TokenServicePort,
            pin_storage: PinStoragePort
    ):
        self.user_repo = user_repo
        self.token_service = token_service
        self.pin_storage = pin_storage

    async def setup_pin(
            self,
            user_id: UUID,
            pin_code: str,
            device_id: str,
            device_name: str
    ) -> dict[str, Any]:
        """Установить PIN для устройства"""

        # Проверяем, что пользователь существует
        user = await self.user_repo.get(UserById(user_id))
        if not user or not user.is_active:
            raise ValueError("User not found or inactive")

        # Хешируем PIN с device_id как соль
        pin_hash = self._hash_pin(pin_code, device_id)

        # Генерируем уникальный токен устройства
        device_token = self._generate_device_token(user_id, device_id)

        # Сохраняем в хранилище
        await self.pin_storage.save_pin(
            user_id=user_id,
            device_id=device_id,
            pin_hash=pin_hash,
            device_name=device_name,
            device_token=device_token,
            ttl=self.PIN_TTL
        )

        # ВАЖНО: Обновляем refresh_token пользователя с device_token
        # Нужно добавить метод для обновления токенов

        return {
            "device_token": device_token,
            "pin_expires_at": datetime.now(UTC) + self.PIN_TTL,
            "message": "PIN set successfully. Please re-login to activate PIN authentication."
        }

    async def verify_pin(
            self,
            pin_code: str,
            device_id: str,
            refresh_token: str
    ) -> dict[str, str] | None:
        """Проверить PIN и выдать новые токены с ротацией"""

        # Декодируем refresh token
        try:
            payload = await self.token_service.decode_token(refresh_token)
            user_id = UUID(payload["sub"])

            # Проверяем blacklist
            if await self.token_service.is_token_blacklisted(refresh_token):
                return None
        except ValueError:
            return None

        # Проверяем количество попыток
        attempts = await self.pin_storage.get_failed_attempts(user_id, device_id)
        if attempts >= self.MAX_ATTEMPTS:
            raise ValueError("Too many failed attempts. Try again later.")

        # Получаем данные PIN
        pin_data = await self.pin_storage.get_pin_data(user_id, device_id)
        if not pin_data:
            return None

        # УБИРАЕМ проверку device_token из payload
        # Вместо этого проверяем только существование PIN для этого устройства

        # Проверяем PIN
        if not self._verify_pin(pin_code, device_id, pin_data["pin_hash"]):
            await self.pin_storage.increment_failed_attempts(user_id, device_id)
            remaining = self.MAX_ATTEMPTS - attempts - 1
            raise ValueError(f"Invalid PIN. {remaining} attempts remaining.")

        # PIN верный - сбрасываем счётчик
        await self.pin_storage.reset_failed_attempts(user_id, device_id)

        # Получаем пользователя
        user = await self.user_repo.get(UserById(user_id))
        if not user or not user.is_active:
            return None

        # Генерируем новые токены с device_token
        jti = str(uuid4())
        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role.name,
            "device_id": device_id,
            "device_token": pin_data["device_token"],  # Теперь добавляем!
            "jti": jti
        }

        # Создаём новые токены
        access_token = await self.token_service.create_access_token(token_data)
        new_refresh_token = await self.token_service.create_refresh_token(token_data)

        # Добавляем старый refresh token в blacklist
        await self.token_service.blacklist_token(
            refresh_token,
            payload.get("exp", 0)
        )

        # Логируем успешный вход
        await self._log_successful_login(user_id, device_id, pin_data.get("device_name"))

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    async def _log_successful_login(
            self,
            user_id: UUID,
            device_id: str,
            device_name: str | None
    ) -> None:
        """Логирование успешного входа для безопасности"""
        # Используем метод порта вместо прямого доступа к redis
        timestamp = datetime.now(UTC).isoformat()
        await self.pin_storage.update_last_login(user_id, device_id, timestamp)

    def _hash_pin(self, pin: str, salt: str) -> str:
        """Хешируем PIN с солью используя PBKDF2"""
        return hashlib.pbkdf2_hmac(
            'sha256',
            pin.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # iterations
        ).hex()

    def _verify_pin(self, pin: str, salt: str, stored_hash: str) -> bool:
        """Безопасное сравнение хешей"""
        return hmac.compare_digest(
            self._hash_pin(pin, salt),
            stored_hash
        )

    def _generate_device_token(self, user_id: UUID, device_id: str) -> str:
        """Генерируем уникальный токен устройства"""
        data = f"{user_id}:{device_id}:{datetime.now().timestamp()}"
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    async def revoke_device(
            self,
            user_id: UUID,
            device_id: str
    ) -> None:
        """Отозвать доступ устройства"""
        # Удаляем PIN
        await self.pin_storage.delete_pin(user_id, device_id)

        # Добавляем в blacklist через метод порта
        await self.pin_storage.add_device_to_blacklist(
            user_id,
            device_id,
            86400 * 365  # 1 год
        )

    async def list_devices(self, user_id: UUID) -> list[dict[str, Any]]:
        """Получить список устройств пользователя"""
        return await self.pin_storage.get_user_devices(user_id)
