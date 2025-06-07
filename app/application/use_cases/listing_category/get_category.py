# app/application/use_cases/listing_category/get_category.py

from app.domain.entities.listing_category import ListingCategory
from app.domain.ports.repositories.listing_category_repository import IListingCategoryRepository
from app.domain.ports.specs.listing_category_specification import ListingCategorySpecificationPort


class GetListingCategoryUseCase:
    """Use case для получения категории"""

    def __init__(self, repo: IListingCategoryRepository):
        self.repo = repo

    async def execute(self, spec: ListingCategorySpecificationPort) -> ListingCategory | None:
        """Получить категорию по спецификации"""
        return await self.repo.get(spec)