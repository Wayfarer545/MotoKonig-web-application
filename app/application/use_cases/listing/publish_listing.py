# app/application/use_cases/listing/publish_listing.py

from uuid import UUID

from app.domain.entities.listing import Listing
from domain.ports.repositories.listing_repository import IListingRepository
from app.infrastructure.specs.listing.listing_by_id import ListingById


class PublishListingUseCase:
    """Use case для публикации объявления"""

    def __init__(self, repo: IListingRepository):
        self.repo = repo

    async def execute(self, listing_id: UUID) -> Listing | None:
        """Опубликовать объявление"""
        listing = await self.repo.get(ListingById(listing_id))

        if not listing:
            return None

        listing.publish()
        return await self.repo.update(listing)
