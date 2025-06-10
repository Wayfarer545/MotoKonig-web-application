# app/application/use_cases/listing/add_to_favorites.py

from uuid import UUID

from app.domain.entities.listing_favorite import ListingFavorite
from app.domain.ports.repositories.listing import IListingRepository
from app.domain.ports.repositories.listing_favorite import IListingFavoriteRepository
from app.infrastructure.specs.listing.listing_by_id import ListingById


class AddToFavoritesUseCase:
    """Use case для добавления в избранное"""

    def __init__(
            self,
            listing_repo: IListingRepository,
            favorite_repo: IListingFavoriteRepository
    ):
        self.listing_repo = listing_repo
        self.favorite_repo = favorite_repo

    async def execute(self, user_id: UUID, listing_id: UUID) -> ListingFavorite:
        """
        Добавить объявление в избранное

        Args:
            user_id: ID пользователя
            listing_id: ID объявления

        Returns:
            ListingFavorite: Созданная запись избранного

        Raises:
            ValueError: При некорректных условиях
        """
        # Проверяем, что объявление существует
        listing = await self.listing_repo.get(ListingById(listing_id))
        if not listing:
            raise ValueError("Listing not found")

        # Нельзя добавить свое объявление в избранное
        if listing.seller_id == user_id:
            raise ValueError("Cannot add own listing to favorites")

        # Проверяем, что объявление видно публично
        if not listing.is_visible_to_public():
            raise ValueError("Cannot add inactive listing to favorites")

        # Проверяем, не добавлено ли уже
        if await self.favorite_repo.is_favorite(user_id, listing_id):
            raise ValueError("Listing already in favorites")

        # Создаем запись избранного
        favorite = ListingFavorite(
            user_id=user_id,
            listing_id=listing_id
        )

        return await self.favorite_repo.add(favorite)