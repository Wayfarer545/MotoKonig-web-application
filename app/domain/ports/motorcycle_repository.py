# app/domain/ports/motorcycle_repository.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.motorcycle import Motorcycle
from app.domain.ports.motorcycle_specification import MotorcycleSpecificationPort


class IMotorcycleRepository(Protocol):
    """Порт репозитория мотоциклов"""

    async def add(self, motorcycle: Motorcycle) -> Motorcycle:
        """Добавить новый мотоцикл"""
        ...

    async def get(self, spec: MotorcycleSpecificationPort) -> Motorcycle | None:
        """Получить мотоцикл по спецификации"""
        ...

    async def get_list(self, spec: MotorcycleSpecificationPort | None = None) -> list[Motorcycle]:
        """Получить список мотоциклов по спецификации"""
        ...

    async def update(self, motorcycle: Motorcycle) -> Motorcycle:
        """Обновить мотоцикл"""
        ...

    async def delete(self, motorcycle_id: UUID) -> bool:
        """Удалить мотоцикл"""
        ...
