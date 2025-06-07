# app/application/use_cases/listing_category/delete_category.py

from uuid import UUID

from app.domain.ports.repositories.listing_category_repository import IListingCategoryRepository


class DeleteListingCategoryUseCase:
    """Use case для удаления категории"""

    def __init__(self, repo: IListingCategoryRepository):
        self.repo = repo

    async def execute(self, category_id: UUID) -> bool:
        """Удалить категорию"""
        return await self.repo.delete(category_id)