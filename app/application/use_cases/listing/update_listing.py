# app/application/use_cases/listing/update_listing.py

from uuid import UUID

from app.domain.entities.listing import Listing
from app.domain.ports.repositories.listing import IListingRepository
from app.domain.value_objects.listing_category import ListingCategory
from app.infrastructure.specs.listing.listing_by_id import ListingById


class UpdateListingUseCase:
    """Use case для обновления объявления"""

    def __init__(self, repo: IListingRepository):
        self.repo = repo

    async def execute(
            self,
            listing_id: UUID,
            title: str | None = None,
            description: str | None = None,
            category: ListingCategory | None = None,
            price: int | None = None,
            location: str | None = None,
            is_negotiable: bool | None = None,
            contact_phone: str | None = None,
            contact_email: str | None = None,
    ) -> Listing | None:
        """Обновить данные объявления"""
        existing = await self.repo.get(ListingById(listing_id))

        if not existing:
            return None

        # Обновляем только переданные поля
        if title is not None:
            existing.update_title(title)
        if description is not None:
            existing.update_description(description)
        if category is not None:
            existing.category = category
        if price is not None:
            existing.update_price(price)
        if location is not None:
            existing._validate_location(location)
            existing.location = location.strip()
        if is_negotiable is not None:
            existing.is_negotiable = is_negotiable
        if contact_phone is not None:
            if contact_phone:
                existing._validate_contact_phone(contact_phone)
                existing.contact_phone = contact_phone.strip()
            else:
                existing.contact_phone = None
        if contact_email is not None:
            existing.contact_email = contact_email.strip() if contact_email else None

        return await self.repo.update(existing)