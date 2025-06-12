# tests/fixtures/enhanced_repositories.py
from __future__ import annotations
from uuid import UUID
from typing import Dict, List, Optional
import asyncio

from app.domain.entities.user import User
from app.domain.entities.motorcycle import Motorcycle
from app.domain.ports.repositories.user import IUserRepository
from app.domain.ports.repositories.motorcycle import IMotorcycleRepository
from app.domain.ports.specs.user import UserSpecificationPort
from app.domain.ports.specs.motorcycle import MotorcycleSpecificationPort
from app.infrastructure.specs.user.user_by_id import UserById
from app.infrastructure.specs.user.user_by_name import UserByName
from app.infrastructure.specs.moto.moto_by_id import MotorcycleById
from app.infrastructure.specs.moto.moto_by_owner import MotorcyclesByOwner


class EnhancedFakeUserRepository(IUserRepository):
    """Улучшенный фейковый репозиторий с реалистичным поведением"""

    def __init__(self):
        self.store: Dict[UUID, User] = {}
        self.call_count = 0
        self.simulate_latency = False
        self.simulate_errors = False
        self.error_on_call = None

    async def add(self, user: User) -> User:
        await self._simulate_db_behavior()

        # Проверка уникальности username
        existing = await self.get(UserByName(user.username))
        if existing:
            raise ValueError(f"User with username '{user.username}' already exists")

        self.store[user.id] = user
        return user

    async def get(self, spec: UserSpecificationPort) -> User | None:
        await self._simulate_db_behavior()

        if isinstance(spec, UserByName):
            for user in self.store.values():
                if user.username == spec.username:
                    return user
        elif isinstance(spec, UserById):
            return self.store.get(spec.user_id)
        return None

    async def get_list(self) -> List[User]:
        await self._simulate_db_behavior()
        return list(self.store.values())

    async def update(self, user: User) -> User:
        await self._simulate_db_behavior()

        if user.id not in self.store:
            raise ValueError(f"User with id {user.id} not found")

        self.store[user.id] = user
        return user

    async def delete(self, user_id: UUID) -> bool:
        await self._simulate_db_behavior()
        return self.store.pop(user_id, None) is not None

    async def _simulate_db_behavior(self):
        """Симуляция поведения реальной БД"""
        self.call_count += 1

        if self.simulate_latency:
            await asyncio.sleep(0.01)  # 10ms задержка

        if self.simulate_errors and self.error_on_call == self.call_count:
            raise Exception("Simulated database error")


class EnhancedFakeMotorcycleRepository(IMotorcycleRepository):
    """Улучшенный фейковый репозиторий мотоциклов"""

    def __init__(self):
        self.store: Dict[UUID, Motorcycle] = {}
        self.call_count = 0

    async def add(self, motorcycle: Motorcycle) -> Motorcycle:
        self.call_count += 1
        self.store[motorcycle.id] = motorcycle
        return motorcycle

    async def get(self, spec: MotorcycleSpecificationPort) -> Motorcycle | None:
        self.call_count += 1

        if isinstance(spec, MotorcycleById):
            return self.store.get(spec.motorcycle_id)
        elif isinstance(spec, MotorcyclesByOwner):
            motorcycles = [m for m in self.store.values() if m.owner_id == spec.owner_id]
            if spec.active_only:
                motorcycles = [m for m in motorcycles if m.is_active]
            return motorcycles[0] if motorcycles else None
        return None

    async def get_list(self, spec: MotorcycleSpecificationPort | None = None) -> List[Motorcycle]:
        self.call_count += 1
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
        self.call_count += 1
        if motorcycle.id not in self.store:
            raise ValueError(f"Motorcycle with id {motorcycle.id} not found")
        self.store[motorcycle.id] = motorcycle
        return motorcycle

    async def delete(self, motorcycle_id: UUID) -> bool:
        self.call_count += 1
        return self.store.pop(motorcycle_id, None) is not None
