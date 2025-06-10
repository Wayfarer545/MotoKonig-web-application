# app/application/controllers/listing_controller.py

from uuid import UUID

from app.application.exceptions import BadRequestError, NotFoundError
from app.application.use_cases.listing.add_to_favorites import AddToFavoritesUseCase
from app.application.use_cases.listing.create_listing import CreateListingUseCase
from app.application.use_cases.listing.delete_listing import DeleteListingUseCase
from app.application.use_cases.listing.get_listing import GetListingUseCase
from app.application.use_cases.listing.list_listings import ListListingsUseCase
from app.application.use_cases.listing.remove_from_favorites import RemoveFromFavoritesUseCase
from app.application.use_cases.listing.update_listing import UpdateListingUseCase
from app.domain.entities.listing import Listing
from app.domain.value_objects.listing_category import ListingCategory
from app.infrastructure.specs.listing.listing_by_id import ListingById
from app.infrastructure.specs.listing.listing_filter import ListingFilter


class ListingController:
    """Контроллер для управления объявлениями"""

    def __init__(
            self,
            create_uc: CreateListingUseCase,
            get_uc: GetListingUseCase,
            list_uc: ListListingsUseCase,
            update_uc: UpdateListingUseCase,
            delete_uc: DeleteListingUseCase,
            add_favorite_uc: AddToFavoritesUseCase,
            remove_favorite_uc: RemoveFromFavoritesUseCase,
    ):
        self.create_uc = create_uc
        self.get_uc = get_uc
        self.list_uc = list_uc
        self.update_uc = update_uc
        self.delete_uc = delete_uc
        self.add_favorite_uc = add_favorite_uc
        self.remove_favorite_uc = remove_favorite_uc

    async def create_listing(
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
        """Создать новое объявление"""
        try:
            return await self.create_uc.execute(
                seller_id=seller_id,
                title=title,
                description=description,
                category=category,
                price=price,
                location=location,
                is_negotiable=is_negotiable,
                contact_phone=contact_phone,
                contact_email=contact_email,
                photo_urls=photo_urls,
            )
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def get_listing_by_id(self, listing_id: UUID) -> dict:
        """Получить объявление по ID"""
        spec = ListingById(listing_id)
        listing = await self.get_uc.execute(spec)

        if not listing:
            raise NotFoundError("Listing not found")

        return listing.to_dto()

    async def get_listing_with_private_info(self, listing_id: UUID) -> dict:
        """Получить объявление с приватной информацией (для владельца)"""
        spec = ListingById(listing_id)
        listing = await self.get_uc.execute(spec)

        if not listing:
            raise NotFoundError("Listing not found")

        return listing.to_dto(include_private_info=True)

    async def search_listings(
            self,
            category: ListingCategory | None = None,
            location: str | None = None,
            price_min: int | None = None,
            price_max: int | None = None,
            search_query: str | None = None,
            seller_id: UUID | None = None,
            active_only: bool = True,
            featured_first: bool = True,
    ) -> list[dict]:
        """Поиск объявлений с фильтрами"""
        spec = ListingFilter(
            category=category,
            location=location,
            price_min=price_min,
            price_max=price_max,
            search_query=search_query,
            seller_id=seller_id,
            active_only=active_only,
            featured_first=featured_first,
        )
        listings = await self.list_uc.execute(spec)
        return [listing.to_dto() for listing in listings]

    async def update_listing(
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
    ) -> dict:
        """Обновить объявление"""
        try:
            updated = await self.update_uc.execute(
                listing_id=listing_id,
                title=title,
                description=description,
                category=category,
                price=price,
                location=location,
                is_negotiable=is_negotiable,
                contact_phone=contact_phone,
                contact_email=contact_email,
            )

            if not updated:
                raise NotFoundError("Listing not found")

            return updated.to_dto(include_private_info=True)
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def delete_listing(self, listing_id: UUID) -> None:
        """Удалить объявление"""
        success = await self.delete_uc.execute(listing_id)
        if not success:
            raise NotFoundError("Listing not found")

    async def add_to_favorites(self, user_id: UUID, listing_id: UUID) -> dict:
        """Добавить объявление в избранное"""
        try:
            favorite = await self.add_favorite_uc.execute(user_id, listing_id)
            return favorite.to_dto()
        except ValueError as ex:
            raise BadRequestError(str(ex)) from ex

    async def remove_from_favorites(self, user_id: UUID, listing_id: UUID) -> None:
        """Удалить объявление из избранного"""
        success = await self.remove_favorite_uc.execute(user_id, listing_id)
        if not success:
            raise NotFoundError("Favorite not found")