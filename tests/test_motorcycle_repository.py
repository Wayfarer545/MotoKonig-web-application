# tests/test_motorcycle_repository.py

from uuid import uuid4

import pytest

from app.domain.entities.motorcycle import Motorcycle
from app.domain.value_objects.engine_type import EngineType
from app.domain.value_objects.motorcycle_type import MotorcycleType
from app.infrastructure.specs.moto.moto_by_id import (
    MotorcycleById,
)
from app.infrastructure.specs.moto.moto_by_owner import (
    MotorcyclesByOwner,
)
from tests.fake_motorcycle_repo import FakeMotorcycleRepository


@pytest.mark.asyncio
async def test_motorcycle_repository_crud():
    """Тест CRUD операций репозитория мотоциклов"""
    repo = FakeMotorcycleRepository()
    owner_id = uuid4()

    # Создание
    motorcycle = Motorcycle(
        owner_id=owner_id,
        brand="Yamaha",
        model="R6",
        year=2022,
        engine_volume=599,
        engine_type=EngineType.INLINE_4,
        motorcycle_type=MotorcycleType.SPORT,
        power=120
    )

    created = await repo.add(motorcycle)
    assert created.id == motorcycle.id
    assert created.brand == "Yamaha"

    # Чтение по ID
    found = await repo.get(MotorcycleById(motorcycle.id))
    assert found is not None
    assert found.id == motorcycle.id

    # Чтение по владельцу
    owner_motorcycles = await repo.get_list(MotorcyclesByOwner(owner_id))
    assert len(owner_motorcycles) == 1
    assert owner_motorcycles[0].id == motorcycle.id

    # Обновление
    motorcycle.power = 130
    updated = await repo.update(motorcycle)
    assert updated.power == 130

    # Удаление
    success = await repo.delete(motorcycle.id)
    assert success is True

    # Проверяем удаление
    deleted = await repo.get(MotorcycleById(motorcycle.id))
    assert deleted is None



