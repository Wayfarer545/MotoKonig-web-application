# app/infrastructure/repositories/sql_listing_favorite_repo.py

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.listing_favorite import ListingFavorite
from app.domain.ports.repositories.listing_favorite import IListingFavoriteRepository
from app.infrastructure.models.listing_favorite import ListingFavorite as ListingFavoriteModel


class SqlListingFavoriteRepository(IListingFavoriteRepository):
    """SQLAlchemy реализация репозитория избранных объявлений"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, favorite: ListingFavorite) -> ListingFavorite:
        """Добавить в избранное"""
        db_favorite = ListingFavoriteModel(
            user_id=favorite.user_id,
            listing_id=favorite.listing_id,
        )

        self.session.add(db_favorite)
        await self.session.flush()
        await self.session.refresh(db_favorite)

        # Обновляем доменную сущность
        favorite.id = db_favorite.id
        favorite.created_at = db_favorite.created_at

        return favorite

    async def remove(self, user_id: UUID, listing_id: UUID) -> bool:
        """Удалить из избранного"""
        statement = select(ListingFavoriteModel).where(
            ListingFavoriteModel.user_id == user_id,
            ListingFavoriteModel.listing_id == listing_id
        )
        result = await self.session.execute(statement)
        db_favorite = result.scalar_one_or_none()

        if db_favorite:
            await self.session.delete(db_favorite)
            await self.session.flush()
            return True

        return False

    async def get_by_user(self, user_id: UUID) -> list[ListingFavorite]:
        """Получить избранное пользователя"""
        statement = select(ListingFavoriteModel).where(
            ListingFavoriteModel.user_id == user_id
        ).order_by(ListingFavoriteModel.created_at.desc())

        result = await self.session.execute(statement)
        favorites = result.scalars().all()

        return [self._to_domain_entity(fav) for fav in favorites]

    async def is_favorite(self, user_id: UUID, listing_id: UUID) -> bool:
        """Проверить, в избранном ли объявление"""
        statement = select(func.count(ListingFavoriteModel.id)).where(
            ListingFavoriteModel.user_id == user_id,
            ListingFavoriteModel.listing_id == listing_id
        )
        result = await self.session.execute(statement)
        count = result.scalar() or 0
        return count > 0

    async def count_by_listing(self, listing_id: UUID) -> int:
        """Подсчитать количество добавлений в избранное"""
        statement = select(func.count(ListingFavoriteModel.id)).where(
            ListingFavoriteModel.listing_id == listing_id
        )
        result = await self.session.execute(statement)
        return result.scalar() or 0

    def _to_domain_entity(self, db_favorite: ListingFavoriteModel) -> ListingFavorite:
        """Преобразовать модель БД в доменную сущность"""
        return ListingFavorite(
            favorite_id=db_favorite.id,
            user_id=db_favorite.user_id,
            listing_id=db_favorite.listing_id,
            created_at=db_favorite.created_at
        )