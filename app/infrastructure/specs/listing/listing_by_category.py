# app/infrastructure/specs/listing/listing_by_category.py

from typing import Any
from uuid import UUID

from domain.ports.specs.listing import ListingSpecificationPort
from app.infrastructure.models.listing_model import Listing as ListingModel


class ListingByCategory(ListingSpecificationPort):
    """Спецификация для поиска объявлений по категории"""

    def __init__(self, category_id: UUID, active_only: bool = True):
        self.category_id = category_id
        self.active_only = active_only

    def to_query(self, base_query: Any) -> Any:
        query = base_query.where(ListingModel.category_id == self.category_id)

        if self.active_only:
            from app.domain.value_objects.listing_status import ListingStatus
            query = query.where(
                ListingModel.status.in_([
                    ListingStatus.ACTIVE,
                    ListingStatus.FEATURED
                ])
            )

        return query.order_by(ListingModel.created_at.desc())
