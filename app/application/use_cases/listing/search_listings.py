# app/application/use_cases/listing/search_listings.py
from uuid import UUID

from app.domain.entities.listing import Listing
from domain.ports.repositories.listing_repository import IListingRepository
from app.infrastructure.specs.listing.listing_search import ListingSearch


class SearchListingsUseCase:
    """Use case для поиска объявлений"""

    def __init__(self, repo: IListingRepository):
        self.repo = repo

    async def execute(
            self,
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
    ) -> list[Listing]:
        """Поиск объявлений с фильтрами"""
        spec = ListingSearch(
            query=query,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            location=location,
            brand=brand,
            model=model,
            year_from=year_from,
            year_to=year_to,
            condition=condition,
            listing_type=listing_type,
            active_only=active_only,
        )

        return await self.repo.get_list(spec)