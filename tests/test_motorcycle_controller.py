# tests/test_motorcycle_controller.py
from uuid import uuid4

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
from app.domain.value_objects.engine_type import EngineType
from app.domain.value_objects.motorcycle_type import MotorcycleType
from tests.fake_motorcycle_repo import FakeMotorcycleRepository


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
