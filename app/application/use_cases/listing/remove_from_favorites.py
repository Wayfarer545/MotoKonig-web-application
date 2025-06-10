# app/application/use_cases/listing/remove_from_favorites.py

from uuid import UUID

from app.domain.ports.repositories.listing_favorite import IListingFavoriteRepository


class RemoveFromFavoritesUseCase:
    """Use case для удаления из избранного"""

    def __init__(self, favorite_repo: IListingFavoriteRepository):
        self.favorite_repo = favorite_repo

    async def execute(self, user_id: UUID, listing_id: UUID) -> bool:
        """Удалить объявление из избранного"""
        return await self.favorite_repo.remove(user_id, listing_id)