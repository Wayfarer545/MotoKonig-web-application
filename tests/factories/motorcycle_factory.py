# tests/factories/motorcycle_factory.py
from uuid import uuid4

from app.domain.entities.motorcycle import Motorcycle
from app.domain.value_objects.engine_type import EngineType
from app.domain.value_objects.motorcycle_type import MotorcycleType


class MotorcycleFactory:
    """Фабрика для создания мотоциклов в тестах"""

    @staticmethod
    def create(**kwargs) -> Motorcycle:
        defaults = {
            "owner_id": uuid4(),
            "brand": "Yamaha",
            "model": "R1",
            "year": 2023,
            "engine_volume": 998,
            "engine_type": EngineType.INLINE_4,
            "motorcycle_type": MotorcycleType.SPORT,
            "power": 200,
            "mileage": 5000,
            "color": "Blue",
            "description": "Test motorcycle"
        }
        defaults.update(kwargs)
        return Motorcycle(**defaults)

    @staticmethod
    def create_sport_bike(**kwargs) -> Motorcycle:
        kwargs.setdefault("motorcycle_type", MotorcycleType.SPORT)
        kwargs.setdefault("power", 180)
        kwargs.setdefault("engine_type", EngineType.INLINE_4)
        return MotorcycleFactory.create(**kwargs)

    @staticmethod
    def create_cruiser(**kwargs) -> Motorcycle:
        kwargs.setdefault("motorcycle_type", MotorcycleType.CRUISER)
        kwargs.setdefault("power", 100)
        kwargs.setdefault("engine_type", EngineType.V_TWIN)
        kwargs.setdefault("brand", "Harley-Davidson")
        return MotorcycleFactory.create(**kwargs)

    @staticmethod
    def create_for_owner(owner_id, count: int = 1, **kwargs) -> list[Motorcycle]:
        kwargs["owner_id"] = owner_id
        return [MotorcycleFactory.create(**kwargs) for _ in range(count)]
