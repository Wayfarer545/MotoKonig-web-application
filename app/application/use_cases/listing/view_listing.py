# app/application/use_cases/listing/view_listing.py

from uuid import UUID

from app.domain.entities.listing import Listing
from domain.ports.repositories.listing_repository import IListingRepository
from app.infrastructure.specs.listing.listing_by_id import ListingById


class ViewListingUseCase:
    """Use case для просмотра объявления с увеличением счетчика"""

    def __init__(self, repo: IListingRepository):
        self.repo = repo

    async def execute(self, listing_id: UUID) -> Listing | None:
        """Просмотреть объявление и увеличить счетчик"""
        listing = await self.repo.get(ListingById(listing_id))

        if not listing:
            return None

        # Увеличиваем счетчик просмотров
        await self.repo.increment_views(listing_id)
        listing.increment_views()

        return listing