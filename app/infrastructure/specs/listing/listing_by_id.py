# app/infrastructure/specs/listing/listing_by_id.py

from typing import Any
from uuid import UUID

from app.domain.ports.specs.listing import ListingSpecificationPort
from app.infrastructure.models.listing import Listing as ListingModel


class ListingById(ListingSpecificationPort):
    """Спецификация для поиска объявления по ID"""

    def __init__(self, listing_id: UUID):
        self.listing_id = listing_id

    def to_query(self, base_query: Any) -> Any:
        return base_query.where(ListingModel.id == self.listing_id)
