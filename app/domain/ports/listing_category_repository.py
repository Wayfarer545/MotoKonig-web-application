# app/domain/ports/listing_category_repository.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.listing_category import ListingCategory
from app.domain.ports.listing_category_specification import ListingCategorySpecificationPort


class IListingCategoryRepository(Protocol):
    """Порт репозитория категорий объявлений"""

    async def add(self, category: ListingCategory) -> ListingCategory:
        """Добавить новую категорию"""
        ...

    async def get(self, spec: ListingCategorySpecificationPort) -> ListingCategory | None:
        """Получить категорию по спецификации"""
        ...

    async def get_list(self, spec: ListingCategorySpecificationPort | None = None) -> list[ListingCategory]:
        """Получить список категорий по спецификации"""
        ...

    async def update(self, category: ListingCategory) -> ListingCategory:
        """Обновить категорию"""
        ...

    async def delete(self, category_id: UUID) -> bool:
        """Удалить категорию"""
        ...

    async def get_root_categories(self) -> list[ListingCategory]:
        """Получить корневые категории"""
        ...

    async def get_subcategories(self, parent_id: UUID) -> list[ListingCategory]:
        """Получить подкатегории"""
        ...

    async def check_slug_exists(self, slug: str, exclude_id: UUID | None = None) -> bool:
        """Проверить существование slug"""
        ...