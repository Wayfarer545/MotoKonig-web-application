# app/infrastructure/specifications/motorcycle_specs/motorcycle_by_brand.py

from typing import Any

from app.domain.ports.motorcycle_specification import MotorcycleSpecificationPort
from app.infrastructure.models.motorcycle_model import Motorcycle as MotorcycleModel


class MotorcyclesByBrand(MotorcycleSpecificationPort):
    """Спецификация для поиска мотоциклов по бренду"""

    def __init__(self, brand: str, active_only: bool = True):
        self.brand = brand.strip().title()
        self.active_only = active_only

    def to_query(self, base_query: Any) -> Any:
        query = base_query.where(MotorcycleModel.brand.ilike(f"%{self.brand}%"))
        if self.active_only:
            query = query.where(MotorcycleModel.is_active == True)
        return query