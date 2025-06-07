# app/infrastructure/specs/listing/listing_search.py

from typing import Any
from uuid import UUID

from domain.ports.specs.listing import ListingSpecificationPort
from app.infrastructure.models.listing_model import Listing as ListingModel


class ListingSearch(ListingSpecificationPort):
    """Комплексная спецификация для поиска объявлений с фильтрами"""

    def __init__(
            self,
            *,
            query: str | None = None,
            category_id: UUID | None = None,
            min_price: float | None = None,
            max_price: float | None = None,
            location: str | None = None,
            brand: str | None = None,
            model: str | None = None,
            year_from: int | None = None,
            year_to: int | None = None,
            condition: str | None = None,
            listing_type: str | None = None,
            active_only: bool = True,
    ):
        self.query = query.strip() if query else None
        self.category_id = category_id
        self.min_price = min_price
        self.max_price = max_price
        self.location = location.strip() if location else None
        self.brand = brand.strip() if brand else None
        self.model = model.strip() if model else None
        self.year_from = year_from
        self.year_to = year_to
        self.condition = condition
        self.listing_type = listing_type
        self.active_only = active_only

    def to_query(self, base_query: Any) -> Any:
        query = base_query

        # Фильтр по активности
        if self.active_only:
            from app.domain.value_objects.listing_status import ListingStatus
            query = query.where(
                ListingModel.status.in_([
                    ListingStatus.ACTIVE,
                    ListingStatus.FEATURED
                ])
            )

        # Текстовый поиск
        if self.query:
            search_term = f"%{self.query}%"
            query = query.where(
                ListingModel.title.ilike(search_term) |
                ListingModel.description.ilike(search_term) |
                ListingModel.brand.ilike(search_term) |
                ListingModel.model.ilike(search_term)
            )

        # Фильтр по категории
        if self.category_id:
            query = query.where(ListingModel.category_id == self.category_id)

        # Фильтр по цене
        if self.min_price is not None:
            query = query.where(ListingModel.price >= self.min_price)
        if self.max_price is not None:
            query = query.where(ListingModel.price <= self.max_price)

        # Фильтр по локации
        if self.location:
            query = query.where(ListingModel.location.ilike(f"%{self.location}%"))

        # Фильтр по бренду
        if self.brand:
            query = query.where(ListingModel.brand.ilike(f"%{self.brand}%"))

        # Фильтр по модели
        if self.model:
            query = query.where(ListingModel.model.ilike(f"%{self.model}%"))

        # Фильтр по году
        if self.year_from:
            query = query.where(ListingModel.year >= self.year_from)
        if self.year_to:
            query = query.where(ListingModel.year <= self.year_to)

        # Фильтр по состоянию
        if self.condition:
            query = query.where(ListingModel.condition == self.condition)

        # Фильтр по типу объявления
        if self.listing_type:
            from app.domain.value_objects.listing_type import ListingType
            query = query.where(ListingModel.listing_type == ListingType(self.listing_type))

        # Сортировка: сначала рекомендуемые, потом по дате
        return query.order_by(
            ListingModel.is_featured.desc(),
            ListingModel.created_at.desc()
        )
