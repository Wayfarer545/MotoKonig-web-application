# app/infrastructure/specifications/motorcycle_specs/motorcycle_search.py

from typing import Any

from app.domain.entities.motorcycle import EngineType, MotorcycleType
from app.domain.ports.motorcycle_specification import MotorcycleSpecificationPort
from app.infrastructure.models.motorcycle_model import Motorcycle as MotorcycleModel


class MotorcycleSearch(MotorcycleSpecificationPort):
    """Комплексная спецификация для поиска мотоциклов с фильтрами"""

    def __init__(
            self,
            *,
            brand: str | None = None,
            model: str | None = None,
            year_from: int | None = None,
            year_to: int | None = None,
            motorcycle_type: MotorcycleType | None = None,
            engine_type: EngineType | None = None,
            engine_volume_from: int | None = None,
            engine_volume_to: int | None = None,
            power_from: int | None = None,
            power_to: int | None = None,
            active_only: bool = True
    ):
        self.brand = brand.strip().title() if brand else None
        self.model = model.strip() if model else None
        self.year_from = year_from
        self.year_to = year_to
        self.motorcycle_type = motorcycle_type
        self.engine_type = engine_type
        self.engine_volume_from = engine_volume_from
        self.engine_volume_to = engine_volume_to
        self.power_from = power_from
        self.power_to = power_to
        self.active_only = active_only

    def to_query(self, base_query: Any) -> Any:
        query = base_query

        if self.active_only:
            query = query.where(MotorcycleModel.is_active == True)

        if self.brand:
            query = query.where(MotorcycleModel.brand.ilike(f"%{self.brand}%"))

        if self.model:
            query = query.where(MotorcycleModel.model.ilike(f"%{self.model}%"))

        if self.year_from:
            query = query.where(MotorcycleModel.year >= self.year_from)

        if self.year_to:
            query = query.where(MotorcycleModel.year <= self.year_to)

        if self.motorcycle_type:
            query = query.where(MotorcycleModel.motorcycle_type == self.motorcycle_type)

        if self.engine_type:
            query = query.where(MotorcycleModel.engine_type == self.engine_type)

        if self.engine_volume_from:
            query = query.where(MotorcycleModel.engine_volume >= self.engine_volume_from)

        if self.engine_volume_to:
            query = query.where(MotorcycleModel.engine_volume <= self.engine_volume_to)

        if self.power_from:
            query = query.where(MotorcycleModel.power >= self.power_from)

        if self.power_to:
            query = query.where(MotorcycleModel.power <= self.power_to)

        return query