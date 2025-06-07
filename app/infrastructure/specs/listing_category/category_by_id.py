# app/infrastructure/specs/listing_category/category_by_id.py

from typing import Any
from uuid import UUID

from app.domain.ports.specs.listing_category_specification import ListingCategorySpecificationPort
from app.infrastructure.models.listing_category_model import ListingCategory as ListingCategoryModel


class CategoryById(ListingCategorySpecificationPort):
    """Спецификация для поиска категории по ID"""

    def __init__(self, category_id: UUID):
        self.category_id = category_id

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(ListingCategoryModel.id == self.category_id)