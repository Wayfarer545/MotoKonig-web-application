# app/infrastructure/specs/listing/listing_filter.py

from typing import Any
from uuid import UUID

from app.domain.ports.specs.listing import ListingSpecificationPort
from app.domain.value_objects.listing_category import ListingCategory
from app.domain.value_objects.listing_status import ListingStatus
from app.infrastructure.models.listing import Listing as ListingModel


class ListingFilter(ListingSpecificationPort):
    """Комплексная спецификация для поиска объявлений с фильтрами"""

    def __init__(
            self,
            *,
            category: ListingCategory | None = None,
            location: str | None = None,
            price_min: int | None = None,
            price_max: int | None = None,
            search_query: str | None = None,
            seller_id: UUID | None = None,
            status: ListingStatus | None = None,
            active_only: bool = True,
            featured_first: bool = True,
    ):
        self.category = category
        self.location = location.strip() if location else None
        self.price_min = price_min
        self.price_max = price_max
        self.search_query = search_query.strip() if search_query else None
        self.seller_id = seller_id
        self.status = status
        self.active_only = active_only
        self.featured_first = featured_first

    def to_query(self, base_query: Any) -> Any:
        query = base_query

        if self.active_only:
            query = query.where(ListingModel.status == ListingStatus.ACTIVE)
        elif self.status:
            query = query.where(ListingModel.status == self.status)

        if self.category:
            query = query.where(ListingModel.category == self.category)

        if self.location:
            query = query.where(ListingModel.location.ilike(f"%{self.location}%"))

        if self.price_min is not None:
            query = query.where(ListingModel.price >= self.price_min)

        if self.price_max is not None:
            query = query.where(ListingModel.price <= self.price_max)

        if self.seller_id:
            query = query.where(ListingModel.seller_id == self.seller_id)

        if self.search_query:
            search_term = f"%{self.search_query}%"
            query = query.where(
                (ListingModel.title.ilike(search_term)) |
                (ListingModel.description.ilike(search_term))
            )

        # Сортировка: сначала рекомендуемые, потом по дате
        if self.featured_first:
            query = query.order_by(
                ListingModel.is_featured.desc(),
                ListingModel.created_at.desc()
            )
        else:
            query = query.order_by(ListingModel.created_at.desc())

        return query
