# app/infrastructure/di/providers/infrastructure/listing.py

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.ports.repositories.listing import IListingRepository
from app.domain.ports.repositories.listing_favorite import IListingFavoriteRepository
from app.infrastructure.repositories.sql_listing_repo import SqlListingRepository
from app.infrastructure.repositories.sql_listing_favorite_repo import SqlListingFavoriteRepository


class ListingRepoProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_listing_repo(self, session: AsyncSession) -> IListingRepository:
        return SqlListingRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_listing_favorite_repo(self, session: AsyncSession) -> IListingFavoriteRepository:
        return SqlListingFavoriteRepository(session)