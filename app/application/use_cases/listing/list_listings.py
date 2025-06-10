# app/application/use_cases/listing/list_listings.py

from app.domain.entities.listing import Listing
from app.domain.ports.repositories.listing import IListingRepository
from app.domain.ports.specs.listing import ListingSpecificationPort


class ListListingsUseCase:
    """Use case для получения списка объявлений"""

    def __init__(self, repo: IListingRepository):
        self.repo = repo

    async def execute(self, spec: ListingSpecificationPort | None = None) -> list[Listing]:
        """Получить список объявлений"""
        return await self.repo.get_list(spec)
