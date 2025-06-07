# app/domain/ports/listing_repository.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.listing import Listing
from domain.ports.specs.listing import ListingSpecificationPort


class IListingRepository(Protocol):
    """Порт репозитория объявлений"""

    async def add(self, listing: Listing) -> Listing:
        """Добавить новое объявление"""
        ...

    async def get(self, spec: ListingSpecificationPort) -> Listing | None:
        """Получить объявление по спецификации"""
        ...

    async def get_list(self, spec: ListingSpecificationPort | None = None) -> list[Listing]:
        """Получить список объявлений по спецификации"""
        ...

    async def update(self, listing: Listing) -> Listing:
        """Обновить объявление"""
        ...

    async def delete(self, listing_id: UUID) -> bool:
        """Удалить объявление"""
        ...

    async def increment_views(self, listing_id: UUID) -> None:
        """Увеличить счетчик просмотров"""
        ...

    async def get_featured_listings(self, limit: int = 10) -> list[Listing]:
        """Получить рекомендуемые объявления"""
        ...
