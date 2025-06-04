# app/domain/ports/pin_storage.py

from typing import Protocol, Dict, Any, Optional, List
from uuid import UUID
from datetime import timedelta


class PinStoragePort(Protocol):
    """Порт для работы с PIN-кодами"""

    async def save_pin(
            self,
            user_id: UUID,
            device_id: str,
            pin_hash: str,
            device_name: str,
            device_token: str,
            ttl: timedelta
    ) -> None:
        """Сохранить PIN для устройства"""
        ...

    async def get_pin_data(
            self,
            user_id: UUID,
            device_id: str
    ) -> Optional[Dict[str, Any]]:
        """Получить данные PIN"""
        ...

    async def delete_pin(
            self,
            user_id: UUID,
            device_id: str
    ) -> None:
        """Удалить PIN"""
        ...

    async def increment_failed_attempts(
            self,
            user_id: UUID,
            device_id: str
    ) -> int:
        """Увеличить счётчик неудачных попыток"""
        ...

    async def get_failed_attempts(
            self,
            user_id: UUID,
            device_id: str
    ) -> int:
        """Получить количество неудачных попыток"""
        ...

    async def reset_failed_attempts(
            self,
            user_id: UUID,
            device_id: str
    ) -> None:
        """Сбросить счётчик попыток"""
        ...

    async def update_last_login(
            self,
            user_id: UUID,
            device_id: str,
            timestamp: str
    ) -> None:
        """Обновить время последнего входа"""
        ...

    async def get_user_devices(
            self,
            user_id: UUID
    ) -> List[Dict[str, Any]]:
        """Получить все устройства пользователя"""
        ...

    async def add_device_to_blacklist(
            self,
            user_id: UUID,
            device_id: str,
            ttl: int
    ) -> None:
        """Добавить устройство в чёрный список"""
        ...