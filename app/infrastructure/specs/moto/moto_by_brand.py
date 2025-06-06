# app/infrastructure/specs/moto/moto_by_brand.py

from typing import Any

from domain.ports.specs.motorcycle import MotorcycleSpecificationPort

from app.infrastructure.models.motorcycle import Motorcycle as MotorcycleModel


class MotorcyclesByBrand(MotorcycleSpecificationPort):
    """Спецификация для поиска мотоциклов по бренду"""

    def __init__(self, brand: str, active_only: bool = True):
        self.brand = brand.strip().title()
        self.active_only = active_only

    def to_query(self, base_query: Any) -> Any:
        query = base_query.where(MotorcycleModel.brand.ilike(f"%{self.brand}%"))
        if self.active_only:
            query = query.where(MotorcycleModel.is_active)
        return query
