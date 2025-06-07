# app/application/use_cases/listing_category/list_categories.py

from app.domain.entities.listing_category import ListingCategory
from app.domain.ports.repositories.listing_category_repository import IListingCategoryRepository
from app.domain.ports.specs.listing_category_specification import ListingCategorySpecificationPort


class ListListingCategoriesUseCase:
    """Use case для получения списка категорий"""

    def __init__(self, repo: IListingCategoryRepository):
        self.repo = repo

    async def execute(self, spec: ListingCategorySpecificationPort | None = None) -> list[ListingCategory]:
        """Получить список категорий"""
        return await self.repo.get_list(spec)