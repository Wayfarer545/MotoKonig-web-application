# app/domain/ports/repositories/ride.py

from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.ride import Ride
from app.domain.ports.specs.ride import RideSpecificationPort

__all__ = ["IRideRepository"]


class IRideRepository(ABC):
    """Порт репозитория для поездок"""

    @abstractmethod
    async def add(self, ride: Ride) -> Ride:
        """Создать новую поездку"""
        ...

    @abstractmethod
    async def get(self, spec: RideSpecificationPort) -> Ride | None:
        """Получить поездку по спецификации"""
        ...

    @abstractmethod
    async def get_by_id(self, ride_id: UUID) -> Ride | None:
        """Получить поездку по ID"""
        ...

    @abstractmethod
    async def get_list(self, spec: RideSpecificationPort | None = None) -> list[Ride]:
        """Получить список поездок по спецификации"""
        ...

    @abstractmethod
    async def update(self, ride: Ride) -> Ride:
        """Обновить поездку"""
        ...

    @abstractmethod
    async def delete(self, ride_id: UUID) -> None:
        """Удалить поездку"""
        ...

    @abstractmethod
    async def get_upcoming_rides(self, limit: int = 10) -> list[Ride]:
        """Получить предстоящие поездки"""
        ...

    @abstractmethod
    async def get_rides_by_organizer(self, organizer_id: UUID) -> list[Ride]:
        """Получить поездки организатора"""
        ...

    @abstractmethod
    async def get_rides_by_participant(self, motokonig_id: UUID) -> list[Ride]:
        """Получить поездки участника"""
        ...
