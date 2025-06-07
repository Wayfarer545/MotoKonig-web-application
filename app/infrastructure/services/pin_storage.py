# app/infrastructure/services/pin_storage.py

from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import UUID

from domain.ports.repositories.pin_storage import PinStoragePort
from redis.asyncio import Redis


class RedisPinStorage(PinStoragePort):
    """Redis реализация хранилища PIN-кодов"""

    def __init__(self, redis: Redis):
        self.redis = redis

    async def save_pin(
            self,
            user_id: UUID,
            device_id: str,
            pin_hash: str,
            device_name: str,
            device_token: str,
            ttl: timedelta
    ) -> None:
        key = f"pin:{user_id}:{device_id}"
        data = {
            "pin_hash": pin_hash,
            "device_name": device_name,
            "device_token": device_token,
            "created_at": datetime.now(UTC).isoformat()
        }

        await self.redis.hset(key, mapping=data)
        await self.redis.expire(key, int(ttl.total_seconds()))

    async def get_pin_data(
            self,
            user_id: UUID,
            device_id: str
    ) -> dict[str, Any] | None:
        key = f"pin:{user_id}:{device_id}"
        data = await self.redis.hgetall(key)
        return data if data else None

    async def delete_pin(
            self,
            user_id: UUID,
            device_id: str
    ) -> None:
        key = f"pin:{user_id}:{device_id}"
        await self.redis.delete(key)

    async def increment_failed_attempts(
            self,
            user_id: UUID,
            device_id: str
    ) -> int:
        key = f"pin_attempts:{user_id}:{device_id}"
        count = await self.redis.incr(key)
        await self.redis.expire(key, 3600)  # 1 час
        return count

    async def get_failed_attempts(
            self,
            user_id: UUID,
            device_id: str
    ) -> int:
        key = f"pin_attempts:{user_id}:{device_id}"
        count = await self.redis.get(key)
        return int(count) if count else 0

    async def reset_failed_attempts(
            self,
            user_id: UUID,
            device_id: str
    ) -> None:
        key = f"pin_attempts:{user_id}:{device_id}"
        await self.redis.delete(key)

    async def get_user_devices(self, user_id: UUID) -> list[dict[str, Any]]:
        """Получить все устройства пользователя"""
        pattern = f"pin:{user_id}:*"
        devices = []

        async for key in self.redis.scan_iter(match=pattern):
            device_data = await self.redis.hgetall(key)
            if device_data:
                device_id = key.split(":")[-1]
                devices.append({
                    "device_id": device_id,
                    "device_name": device_data.get("device_name"),
                    "created_at": device_data.get("created_at"),
                    "last_login": device_data.get("last_login")
                })

        return devices

    async def update_last_login(
            self,
            user_id: UUID,
            device_id: str,
            timestamp: str
    ) -> None:
        """Обновить время последнего входа"""
        key = f"pin:{user_id}:{device_id}"
        await self.redis.hset(key, "last_login", timestamp)

    async def add_device_to_blacklist(
            self,
            user_id: UUID,
            device_id: str,
            ttl: int
    ) -> None:
        """Добавить устройство в чёрный список"""
        key = f"blacklisted_device:{user_id}:{device_id}"
        await self.redis.set(key, "1", ex=ttl)
