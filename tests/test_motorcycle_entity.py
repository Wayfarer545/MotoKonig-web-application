# tests/test_motorcycle_entity.py

from datetime import datetime
from uuid import uuid4

import pytest

from app.domain.entities.motorcycle import Motorcycle
from app.domain.value_objects.motorcycle_type import MotorcycleType
from app.domain.value_objects.engine_type import EngineType


def test_motorcycle_creation_valid():
    """Тест создания валидного мотоцикла"""
    owner_id = uuid4()
    motorcycle = Motorcycle(
        owner_id=owner_id,
        brand="Yamaha",
        model="R1",
        year=2023,
        engine_volume=998,
        engine_type=EngineType.INLINE_4,
        motorcycle_type=MotorcycleType.SPORT,
        power=200,
        mileage=5000,
        color="Blue",
        description="Amazing sportbike"
    )

    assert motorcycle.owner_id == owner_id
    assert motorcycle.brand == "Yamaha"
    assert motorcycle.model == "R1"
    assert motorcycle.year == 2023
    assert motorcycle.engine_volume == 998
    assert motorcycle.engine_type == EngineType.INLINE_4
    assert motorcycle.motorcycle_type == MotorcycleType.SPORT
    assert motorcycle.power == 200
    assert motorcycle.mileage == 5000
    assert motorcycle.color == "Blue"
    assert motorcycle.description == "Amazing sportbike"
    assert motorcycle.is_active is True


def test_motorcycle_validation_errors():
    """Тест валидации мотоцикла"""
    owner_id = uuid4()

    # Невалидный год
    with pytest.raises(ValueError, match="Year cannot be before 1885"):
        Motorcycle(
            owner_id=owner_id,
            brand="Yamaha",
            model="R1",
            year=1800,
            engine_volume=998,
            engine_type=EngineType.INLINE_4,
            motorcycle_type=MotorcycleType.SPORT
        )

    # Год в будущем
    future_year = datetime.now().year + 5
    with pytest.raises(ValueError, match="Year cannot be in the future"):
        Motorcycle(
            owner_id=owner_id,
            brand="Yamaha",
            model="R1",
            year=future_year,
            engine_volume=998,
            engine_type=EngineType.INLINE_4,
            motorcycle_type=MotorcycleType.SPORT
        )

    # Невалидный объем двигателя
    with pytest.raises(ValueError, match="Engine volume must be positive"):
        Motorcycle(
            owner_id=owner_id,
            brand="Yamaha",
            model="R1",
            year=2023,
            engine_volume=0,
            engine_type=EngineType.INLINE_4,
            motorcycle_type=MotorcycleType.SPORT
        )

    # Пустая марка
    with pytest.raises(ValueError, match="Brand cannot be empty"):
        Motorcycle(
            owner_id=owner_id,
            brand="",
            model="R1",
            year=2023,
            engine_volume=998,
            engine_type=EngineType.INLINE_4,
            motorcycle_type=MotorcycleType.SPORT
        )


def test_motorcycle_business_methods():
    """Тест бизнес-методов мотоцикла"""
    owner_id = uuid4()
    motorcycle = Motorcycle(
        owner_id=owner_id,
        brand="kawasaki",
        model="ninja",
        year=2023,
        engine_volume=998,
        engine_type=EngineType.INLINE_4,
        motorcycle_type=MotorcycleType.SPORT,
        power=200,
        mileage=5000
    )

    # Проверяем нормализацию
    assert motorcycle.brand == "Kawasaki"
    assert motorcycle.model == "ninja"

    # Тест обновления пробега
    motorcycle.update_mileage(6000)
    assert motorcycle.mileage == 6000

    # Попытка уменьшить пробег
    with pytest.raises(ValueError, match="New mileage cannot be less than current mileage"):
        motorcycle.update_mileage(5000)

    # Тест деактивации/активации
    motorcycle.deactivate()
    assert motorcycle.is_active is False

    motorcycle.activate()
    assert motorcycle.is_active is True

    # Тест display_name
    assert motorcycle.get_display_name() == "Kawasaki ninja (2023)"

    # Тест engine_info
    engine_info = motorcycle.get_engine_info()
    assert "998cc" in engine_info
    assert "Inline 4" in engine_info
    assert "200 hp" in engine_info


def test_motorcycle_to_dto():
    """Тест конвертации в DTO"""
    owner_id = uuid4()
    motorcycle = Motorcycle(
        owner_id=owner_id,
        brand="Honda",
        model="CBR1000RR",
        year=2023,
        engine_volume=1000,
        engine_type=EngineType.INLINE_4,
        motorcycle_type=MotorcycleType.SPORT,
        power=215
    )

    dto = motorcycle.to_dto()

    assert dto["owner_id"] == owner_id
    assert dto["brand"] == "Honda"
    assert dto["model"] == "CBR1000RR"
    assert dto["year"] == 2023
    assert dto["engine_volume"] == 1000
    assert dto["engine_type"] == EngineType.INLINE_4
    assert dto["motorcycle_type"] == MotorcycleType.SPORT
    assert dto["power"] == 215
    assert dto["is_active"] is True
    assert "display_name" in dto
    assert "engine_info" in dto


# tests/test_motorcycle_repository.py


from app.infrastructure.specifications.motorcycle_specs.motorcycle_by_id import (
    MotorcycleById,
)
from app.infrastructure.specifications.motorcycle_specs.motorcycle_by_owner import (
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


# tests/test_motorcycle_controller.py

import pytest

from app.application.controllers.motorcycle_controller import MotorcycleController
from app.application.exceptions import NotFoundError
from app.application.use_cases.motorcycle.create_motorcycle import (
    CreateMotorcycleUseCase,
)
from app.application.use_cases.motorcycle.delete_motorcycle import (
    DeleteMotorcycleUseCase,
)
from app.application.use_cases.motorcycle.get_motorcycle import GetMotorcycleUseCase
from app.application.use_cases.motorcycle.list_motorcycles import ListMotorcyclesUseCase
from app.application.use_cases.motorcycle.update_motorcycle import (
    UpdateMotorcycleUseCase,
)


@pytest.mark.asyncio
async def test_motorcycle_controller():
    """Тест контроллера мотоциклов"""
    repo = FakeMotorcycleRepository()

    # Создаем use cases
    list_uc = ListMotorcyclesUseCase(repo)
    get_uc = GetMotorcycleUseCase(repo)
    create_uc = CreateMotorcycleUseCase(repo)
    update_uc = UpdateMotorcycleUseCase(repo)
    delete_uc = DeleteMotorcycleUseCase(repo)

    # Создаем контроллер
    controller = MotorcycleController(list_uc, get_uc, create_uc, update_uc, delete_uc)

    owner_id = uuid4()

    # Создание мотоцикла
    motorcycle = await controller.create_motorcycle(
        owner_id=owner_id,
        brand="Ducati",
        model="Panigale V4",
        year=2023,
        engine_volume=1103,
        engine_type=EngineType.V4,
        motorcycle_type=MotorcycleType.SPORT,
        power=215
    )

    assert motorcycle.brand == "Ducati"
    assert motorcycle.model == "Panigale V4"

    # Получение мотоцикла
    dto = await controller.get_motorcycle_by_id(motorcycle.id)
    assert dto["brand"] == "Ducati"

    # Получение мотоциклов пользователя
    user_motorcycles = await controller.get_user_motorcycles(owner_id)
    assert len(user_motorcycles) == 1

    # Обновление
    updated_dto = await controller.update_motorcycle(
        motorcycle.id,
        power=220,
        description="Updated description"
    )
    assert updated_dto["power"] == 220
    assert updated_dto["description"] == "Updated description"

    # Удаление
    await controller.delete_motorcycle(motorcycle.id)

    # Проверяем, что мотоцикл удален
    with pytest.raises(NotFoundError):
        await controller.get_motorcycle_by_id(motorcycle.id)
