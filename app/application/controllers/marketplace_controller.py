# app/application/controllers/marketplace_controller.py

from decimal import Decimal
from uuid import UUID

from app.application.exceptions import BadRequestError, NotFoundError
from app.application.use_cases.listing.create_listing import CreateListingUseCase
from app.application.use_cases.listing.delete_listing import DeleteListingUseCase
from app.application.use_cases.listing.get_listing import GetListingUseCase
from app.application.use_cases.listing.list_listings import ListListingsUseCase
from app.application.use_cases.listing.publish_listing import PublishListingUseCase
from app.application.use_cases.listing.search_listings import SearchListingsUseCase
from app.application.use_cases.listing.update_listing import UpdateListingUseCase
from app.application.use_cases.listing.view_listing import ViewListingUseCase
from app.application.use_cases.listing_category.create_category import (
    CreateListingCategoryUseCase,
)
from app.domain.value_objects.listing_type import ListingType
from app.infrastructure.specs.listing.listing_by_id import ListingById
from app.infrastructure.specs.listing.listing_by_seller import ListingBySeller
from app.infrastructure.specs.listing_category.category_by_id import CategoryById


class MarketplaceController:
    """Контроллер для маркетплейса"""

    def __init__(
            self,
            create_listing_uc: CreateListingUseCase,
            get_listing_uc: GetListingUseCase,
            list_listings_uc: ListListingsUseCase,
            update_listing_uc: UpdateListingUseCase,
            delete_listing_uc: DeleteListingUseCase,
            publish_listing_uc: PublishListingUseCase,
            view_listing_uc: ViewListingUseCase,
            search_listings_uc: SearchListingsUseCase,
            create_category_uc: CreateListingCategoryUseCase,
    ):
        self.create_listing_uc = create_listing_uc
        self.get_listing_uc = get_listing_uc
        self.list_listings_uc = list_listings_uc
        self.update_listing_uc = update_listing_uc
        self.delete_listing_uc = delete_listing_uc
        self.publish_listing_uc = publish_listing_uc
        self.view_listing_uc = view_listing_uc
        self.search_listings_uc = search_listings_uc
        self.create_category_uc = create_category_uc

    async def create_listing(
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
    ) -> dict:
        """Создать новое объявление"""
        try:
            listing = await self.create_listing_uc.execute(
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
            return listing.to_dto()
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def get_listing_by_id(self, listing_id: UUID, increment_views: bool = False) -> dict:
        """Получить объявление по ID"""
        if increment_views:
            listing = await self.view_listing_uc.execute(listing_id)
        else:
            listing = await self.get_listing_uc.execute(ListingById(listing_id))

        if not listing:
            raise NotFoundError("Listing not found")

        return listing.to_dto()

    async def get_seller_listings(
            self,
            seller_id: UUID,
            active_only: bool = True
    ) -> list[dict]:
        """Получить объявления продавца"""
        spec = ListingBySeller(seller_id, active_only)
        listings = await self.list_listings_uc.execute(spec)
        return [listing.to_dto() for listing in listings]

    async def search_listings(
            self,
            query: str | None = None,
            category_id: UUID | None = None,
            min_price: float | None = None,
            max_price: float | None = None,
            location: str | None = None,
            brand: str | None = None,
            model: str | None = None,
            year_from: int | None = None,
            year_to: int | None = None,
            condition: str | None = None,
            listing_type: str | None = None,
            active_only: bool = True,
    ) -> list[dict]:
        """Поиск объявлений с фильтрами"""
        listings = await self.search_listings_uc.execute(
            query=query,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            location=location,
            brand=brand,
            model=model,
            year_from=year_from,
            year_to=year_to,
            condition=condition,
            listing_type=listing_type,
            active_only=active_only,
        )
        return [listing.to_dto() for listing in listings]

    async def update_listing(
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
    ) -> dict:
        """Обновить объявление"""
        try:
            updated = await self.update_listing_uc.execute(
                listing_id=listing_id,
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

            if not updated:
                raise NotFoundError("Listing not found")

            return updated.to_dto()
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def publish_listing(self, listing_id: UUID) -> dict:
        """Опубликовать объявление"""
        try:
            published = await self.publish_listing_uc.execute(listing_id)

            if not published:
                raise NotFoundError("Listing not found")

            return published.to_dto()
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def delete_listing(self, listing_id: UUID) -> None:
        """Удалить объявление"""
        success = await self.delete_listing_uc.execute(listing_id)
        if not success:
            raise NotFoundError("Listing not found")

    async def create_category(
            self,
            name: str,
            slug: str,
            description: str | None = None,
            parent_id: UUID | None = None,
            icon: str | None = None,
            sort_order: int = 0,
    ) -> dict:
        """Создать новую категорию"""
        try:
            category = await self.create_category_uc.execute(
                name=name,
                slug=slug,
                description=description,
                parent_id=parent_id,
                icon=icon,
                sort_order=sort_order,
            )
            return category.to_dto()
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex