# app/application/use_cases/listing/create_listing.py

from decimal import Decimal
from uuid import UUID

from app.domain.entities.listing import Listing
from domain.ports.repositories.listing_repository import IListingRepository
from app.domain.value_objects.listing_type import ListingType


class CreateListingUseCase:
    """Use case для создания объявления"""

    def __init__(self, repo: IListingRepository):
        self.repo = repo

    async def execute(
            self,
            seller_id: UUID,
            category_id: UUID,
            title: str,
            description: str,
            price: Decimal,
            listing_type: ListingType = ListingType.SALE,
            location: str | None = None,
            latitude: float | None = None,
            longitude: float | None = None,
            contact_phone: str | None = None,
            contact_email: str | None = None,
            is_negotiable: bool = False,
            condition: str | None = None,
            brand: str | None = None,
            model: str | None = None,
            year: int | None = None,
            mileage: int | None = None,
    ) -> Listing:
        """Создать новое объявление"""
        listing = Listing(
            seller_id=seller_id,
            category_id=category_id,
            title=title,
            description=description,
            price=price,
            listing_type=listing_type,
            location=location,
            latitude=latitude,
            longitude=longitude,
            contact_phone=contact_phone,
            contact_email=contact_email,
            is_negotiable=is_negotiable,
            condition=condition,
            brand=brand,
            model=model,
            year=year,
            mileage=mileage,
        )

        return await self.repo.add(listing)