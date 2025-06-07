# app/application/use_cases/listing/update_listing.py

from decimal import Decimal
from uuid import UUID

from app.domain.entities.listing import Listing
from domain.ports.repositories.listing_repository import IListingRepository
from app.domain.value_objects.listing_type import ListingType
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
            price: Decimal | None = None,
            listing_type: ListingType | None = None,
            location: str | None = None,
            latitude: float | None = None,
            longitude: float | None = None,
            contact_phone: str | None = None,
            contact_email: str | None = None,
            is_negotiable: bool | None = None,
            condition: str | None = None,
            brand: str | None = None,
            model: str | None = None,
            year: int | None = None,
            mileage: int | None = None,
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
        if price is not None:
            existing.update_price(price)
        if listing_type is not None:
            existing.listing_type = listing_type
        if location is not None or latitude is not None or longitude is not None:
            existing.update_location(location, latitude, longitude)
        if contact_phone is not None:
            existing.contact_phone = contact_phone
        if contact_email is not None:
            existing.contact_email = contact_email
        if is_negotiable is not None:
            existing.is_negotiable = is_negotiable
        if condition is not None:
            existing.condition = condition
        if brand is not None:
            existing.brand = brand
        if model is not None:
            existing.model = model
        if year is not None:
            existing.year = year
        if mileage is not None:
            existing.mileage = mileage

        return await self.repo.update(existing)