# app/application/use_cases/listing_category/create_category.py

from uuid import UUID

from app.domain.entities.listing_category import ListingCategory
from app.domain.ports.repositories.listing_category_repository import IListingCategoryRepository


class CreateListingCategoryUseCase:
    """Use case для создания категории объявлений"""

    def __init__(self, repo: IListingCategoryRepository):
        self.repo = repo

    async def execute(
            self,
            name: str,
            slug: str,
            description: str | None = None,
            parent_id: UUID | None = None,
            icon: str | None = None,
            sort_order: int = 0,
    ) -> ListingCategory:
        """Создать новую категорию"""

        # Проверяем уникальность slug
        if await self.repo.check_slug_exists(slug):
            raise ValueError(f"Category with slug '{slug}' already exists")

        category = ListingCategory(
            name=name,
            slug=slug,
            description=description,
            parent_id=parent_id,
            icon=icon,
            sort_order=sort_order,
        )

        return await self.repo.add(category)