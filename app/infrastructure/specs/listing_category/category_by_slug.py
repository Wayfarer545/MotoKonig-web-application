# app/infrastructure/specs/listing_category/category_by_slug.py

from typing import Any

from app.domain.ports.listing_category_specification import ListingCategorySpecificationPort
from app.infrastructure.models.listing_category_model import ListingCategory as ListingCategoryModel


class CategoryBySlug(ListingCategorySpecificationPort):
    """Спецификация для поиска категории по slug"""

    def __init__(self, slug: str):
        self.slug = slug

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(ListingCategoryModel.slug == self.slug)