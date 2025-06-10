# app/application/use_cases/listing/create_listing.py

from uuid import UUID

from app.domain.entities.listing import Listing
from app.domain.ports.repositories.listing import IListingRepository
from app.domain.value_objects.listing_category import ListingCategory
from app.domain.value_objects.listing_status import ListingStatus


class CreateListingUseCase:
    """Use case для создания объявления"""

    def __init__(self, repo: IListingRepository):
        self.repo = repo

    async def execute(
            self,
            seller_id: UUID,
            title: str,
            description: str,
            category: ListingCategory,
            price: int,
            location: str,
            is_negotiable: bool = True,
            contact_phone: str | None = None,
            contact_email: str | None = None,
            photo_urls: list[str] | None = None,
    ) -> Listing:
        """
        Создать новое объявление

        Args:
            seller_id: ID продавца
            title: Название объявления
            description: Описание
            category: Категория товара
            price: Цена в копейках
            location: Местоположение
            is_negotiable: Торг уместен
            contact_phone: Контактный телефон
            contact_email: Контактный email
            photo_urls: Список URL фотографий

        Returns:
            Listing: Созданное объявление

        Raises:
            ValueError: При превышении лимитов или некорректных данных
        """
        # Проверяем лимит активных объявлений
        active_count = await self.repo.count_active_by_seller(seller_id)
        if active_count >= 100:
            raise ValueError("Maximum 100 active listings allowed per user")

        # Создаем объявление
        listing = Listing(
            seller_id=seller_id,
            title=title,
            description=description,
            category=category,
            price=price,
            location=location,
            is_negotiable=is_negotiable,
            contact_phone=contact_phone,
            contact_email=contact_email,
            photo_urls=photo_urls or [],
            status=ListingStatus.DRAFT,
        )

        return await self.repo.add(listing)
