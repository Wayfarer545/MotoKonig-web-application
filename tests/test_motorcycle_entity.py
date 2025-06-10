# tests/test_motorcycle_entity.py

from datetime import datetime
from uuid import uuid4

import pytest

from app.domain.entities.motorcycle import Motorcycle
from app.domain.value_objects.engine_type import EngineType
from app.domain.value_objects.motorcycle_type import MotorcycleType


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



def base_args():
    return dict(
        owner_id=uuid4(),
        brand="Honda",
        model="CBR",
        year=2024,
        engine_volume=1000,
        engine_type=EngineType.INLINE_4,
        motorcycle_type=MotorcycleType.SPORT,
    )


def test_motorcycle_extra_validation():
    with pytest.raises(ValueError):
        Motorcycle(**base_args(), power=-1)
    with pytest.raises(ValueError):
        Motorcycle(**base_args(), power=600)
    with pytest.raises(ValueError):
        Motorcycle(**base_args(), mileage=-5)
    args = base_args(); args["engine_volume"] = 4000
    with pytest.raises(ValueError):
        Motorcycle(**args)
    args = base_args(); args["brand"] = "A"
    with pytest.raises(ValueError):
        Motorcycle(**args)
    args = base_args(); args["model"] = ""
    with pytest.raises(ValueError):
        Motorcycle(**args)


def test_update_description_and_mileage_validation():
    m = Motorcycle(**base_args(), mileage=100, description="  text  ")
    assert m.description == "text"
    m.update_description(" new ")
    assert m.description == "new"
    m.update_description(None)
    assert m.description is None
    with pytest.raises(ValueError):
        m.update_mileage(-1)