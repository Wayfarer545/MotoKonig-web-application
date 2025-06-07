# tests/fake_motorcycle_repo.py

from __future__ import annotations

from uuid import UUID

from app.domain.entities.motorcycle import Motorcycle
from app.domain.ports.epositories.motorcycle_repository import IMotorcycleRepository
from app.domain.ports.specs.motorcycle import MotorcycleSpecificationPort
from app.infrastructure.specs.moto.moto_by_id import (
    MotorcycleById,
)
from app.infrastructure.specs.moto.moto_by_owner import (
    MotorcyclesByOwner,
)


class FakeMotorcycleRepository(IMotorcycleRepository):
    """Фейковый репозиторий мотоциклов для тестов"""

    def __init__(self):
        self.store: dict[UUID, Motorcycle] = {}

    async def add(self, motorcycle: Motorcycle) -> Motorcycle:
        """Добавить мотоцикл"""
        self.store[motorcycle.id] = motorcycle
        return motorcycle

    async def get(self, spec: MotorcycleSpecificationPort) -> Motorcycle | None:
        """Получить мотоцикл по спецификации"""
        if isinstance(spec, MotorcycleById):
            return self.store.get(spec.motorcycle_id)

        # Простая реализация для других спецификаций
        motorcycles = list(self.store.values())

        if isinstance(spec, MotorcyclesByOwner):
            filtered = [m for m in motorcycles if m.owner_id == spec.owner_id]
            if spec.active_only:
                filtered = [m for m in filtered if m.is_active]
            return filtered[0] if filtered else None

        return None

    async def get_list(self, spec: MotorcycleSpecificationPort | None = None) -> list[Motorcycle]:
        """Получить список мотоциклов"""
        motorcycles = list(self.store.values())

        if spec is None:
            return motorcycles

        if isinstance(spec, MotorcyclesByOwner):
            filtered = [m for m in motorcycles if m.owner_id == spec.owner_id]
            if spec.active_only:
                filtered = [m for m in filtered if m.is_active]
            return filtered

        return motorcycles

    async def update(self, motorcycle: Motorcycle) -> Motorcycle:
        """Обновить мотоцикл"""
        self.store[motorcycle.id] = motorcycle
        return motorcycle

    async def delete(self, motorcycle_id: UUID) -> bool:
        """Удалить мотоцикл"""
        return self.store.pop(motorcycle_id, None) is not None
