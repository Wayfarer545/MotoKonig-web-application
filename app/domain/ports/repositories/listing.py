# app/domain/ports/repositories/listing.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.listing import Listing
from app.domain.ports.specs.listing import ListingSpecificationPort


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

    async def count_active_by_seller(self, seller_id: UUID) -> int:
        """Подсчитать активные объявления продавца"""
        ...

    async def expire_old_listings(self) -> int:
        """Пометить старые объявления как истёкшие"""
        ...