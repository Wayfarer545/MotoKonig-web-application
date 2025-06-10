# app/application/use_cases/listing/delete_listing.py

from uuid import UUID

from app.domain.ports.repositories.listing import IListingRepository


class DeleteListingUseCase:
    """Use case для удаления объявления"""

    def __init__(self, repo: IListingRepository):
        self.repo = repo

    async def execute(self, listing_id: UUID) -> bool:
        """Удалить объявление"""
        return await self.repo.delete(listing_id)