# app/application/use_cases/listing_category/update_category.py

from uuid import UUID

from app.domain.entities.listing_category import ListingCategory
from app.domain.ports.repositories.listing_category_repository import IListingCategoryRepository
from app.infrastructure.specs.listing_category.category_by_id import CategoryById


class UpdateListingCategoryUseCase:
    """Use case для обновления категории"""

    def __init__(self, repo: IListingCategoryRepository):
        self.repo = repo

    async def execute(
            self,
            category_id: UUID,
            name: str | None = None,
            slug: str | None = None,
            description: str | None = None,
            parent_id: UUID | None = None,
            icon: str | None = None,
            sort_order: int | None = None,
            is_active: bool | None = None,
    ) -> ListingCategory | None:
        """Обновить данные категории"""
        existing = await self.repo.get(CategoryById(category_id))

        if not existing:
            return None

        # Проверяем уникальность slug если он изменяется
        if slug is not None and slug != existing.slug:
            if await self.repo.check_slug_exists(slug, category_id):
                raise ValueError(f"Category with slug '{slug}' already exists")

        # Обновляем только переданные поля
        if name is not None:
            existing.update_name(name)
        if slug is not None:
            existing.update_slug(slug)
        if description is not None:
            existing.update_description(description)
        if parent_id is not None:
            existing.set_parent(parent_id)
        if icon is not None:
            existing.icon = icon
        if sort_order is not None:
            existing.update_sort_order(sort_order)
        if is_active is not None:
            if is_active:
                existing.activate()
            else:
                existing.deactivate()

        return await self.repo.update(existing)