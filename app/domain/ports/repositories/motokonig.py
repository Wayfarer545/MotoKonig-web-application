# app/domain/ports/repositories/motokonig.py

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.motokonig import MotoKonig
from app.domain.ports.specs.motokonig import MotoKonigSpecificationPort

__all__ = ["IMotoKonigRepository"]


class IMotoKonigRepository(ABC):
    """Порт репозитория для MotoKonig"""

    @abstractmethod
    async def add(self, motokonig: MotoKonig) -> MotoKonig:
        """Добавить новый профиль MotoKonig"""
        ...

    @abstractmethod
    async def get(self, spec: MotoKonigSpecificationPort) -> MotoKonig | None:
        """Получить профиль по спецификации"""
        ...

    @abstractmethod
    async def get_by_id(self, motokonig_id: UUID) -> MotoKonig | None:
        """Получить профиль по ID"""
        ...

    @abstractmethod
    async def get_by_user_id(self, user_id: UUID) -> MotoKonig | None:
        """Получить профиль по ID пользователя"""
        ...

    @abstractmethod
    async def get_list(self, spec: MotoKonigSpecificationPort | None = None) -> list[MotoKonig]:
        """Получить список профилей по спецификации"""
        ...

    @abstractmethod
    async def update(self, motokonig: MotoKonig) -> MotoKonig:
        """Обновить профиль"""
        ...

    @abstractmethod
    async def delete(self, motokonig_id: UUID) -> None:
        """Удалить профиль"""
        ...

    @abstractmethod
    async def exists(self, spec: MotoKonigSpecificationPort) -> bool:
        """Проверить существование профиля по спецификации"""
        ...
