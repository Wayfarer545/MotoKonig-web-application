# app/domain/ports/repositories/listing_favorite.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.listing_favorite import ListingFavorite


class IListingFavoriteRepository(Protocol):
    """Порт репозитория избранных объявлений"""

    async def add(self, favorite: ListingFavorite) -> ListingFavorite:
        """Добавить в избранное"""
        ...

    async def remove(self, user_id: UUID, listing_id: UUID) -> bool:
        """Удалить из избранного"""
        ...

    async def get_by_user(self, user_id: UUID) -> list[ListingFavorite]:
        """Получить избранное пользователя"""
        ...

    async def is_favorite(self, user_id: UUID, listing_id: UUID) -> bool:
        """Проверить, в избранном ли объявление"""
        ...

    async def count_by_listing(self, listing_id: UUID) -> int:
        """Подсчитать количество добавлений в избранное"""
        ...