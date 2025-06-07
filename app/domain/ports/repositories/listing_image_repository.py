# app/domain/ports/listing_image_repository.py

from typing import Protocol
from uuid import UUID

from app.domain.entities.listing_image import ListingImage
from domain.ports.specs.listing_image import ListingImageSpecificationPort


class IListingImageRepository(Protocol):
    """Порт репозитория изображений объявлений"""

    async def add(self, image: ListingImage) -> ListingImage:
        """Добавить новое изображение"""
        ...

    async def get(self, spec: ListingImageSpecificationPort) -> ListingImage | None:
        """Получить изображение по спецификации"""
        ...

    async def get_list(self, spec: ListingImageSpecificationPort | None = None) -> list[ListingImage]:
        """Получить список изображений по спецификации"""
        ...

    async def update(self, image: ListingImage) -> ListingImage:
        """Обновить изображение"""
        ...

    async def delete(self, image_id: UUID) -> bool:
        """Удалить изображение"""
        ...

    async def get_listing_images(self, listing_id: UUID) -> list[ListingImage]:
        """Получить все изображения объявления"""
        ...

    async def get_primary_image(self, listing_id: UUID) -> ListingImage | None:
        """Получить главное изображение объявления"""
        ...

    async def unset_all_primary(self, listing_id: UUID) -> None:
        """Убрать отметку главного у всех изображений объявления"""
        ...

    async def reorder_images(self, listing_id: UUID, image_orders: dict[UUID, int]) -> None:
        """Изменить порядок изображений"""
        ...
