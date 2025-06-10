# app/application/use_cases/listing/get_listing.py

from app.domain.entities.listing import Listing
from app.domain.ports.repositories.listing import IListingRepository
from app.domain.ports.specs.listing import ListingSpecificationPort


class GetListingUseCase:
    """Use case для получения объявления"""

    def __init__(self, repo: IListingRepository):
        self.repo = repo

    async def execute(self, spec: ListingSpecificationPort) -> Listing | None:
        """Получить объявление по спецификации"""
        return await self.repo.get(spec)
