# app/infrastructure/di/providers/use_cases/listing.py

from dishka import Provider, Scope, provide

from app.application.use_cases.listing.add_to_favorites import AddToFavoritesUseCase
from app.application.use_cases.listing.create_listing import CreateListingUseCase
from app.application.use_cases.listing.delete_listing import DeleteListingUseCase
from app.application.use_cases.listing.get_listing import GetListingUseCase
from app.application.use_cases.listing.list_listings import ListListingsUseCase
from app.application.use_cases.listing.remove_from_favorites import RemoveFromFavoritesUseCase
from app.application.use_cases.listing.update_listing import UpdateListingUseCase
from app.domain.ports.repositories.listing import IListingRepository
from app.domain.ports.repositories.listing_favorite import IListingFavoriteRepository


class ListingUseCaseProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_create_listing_uc(self, repo: IListingRepository) -> CreateListingUseCase:
        return CreateListingUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_get_listing_uc(self, repo: IListingRepository) -> GetListingUseCase:
        return GetListingUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_list_listings_uc(self, repo: IListingRepository) -> ListListingsUseCase:
        return ListListingsUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_update_listing_uc(self, repo: IListingRepository) -> UpdateListingUseCase:
        return UpdateListingUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_delete_listing_uc(self, repo: IListingRepository) -> DeleteListingUseCase:
        return DeleteListingUseCase(repo)

    @provide(scope=Scope.REQUEST)
    def provide_add_to_favorites_uc(
        self,
        listing_repo: IListingRepository,
        favorite_repo: IListingFavoriteRepository,
    ) -> AddToFavoritesUseCase:
        return AddToFavoritesUseCase(listing_repo, favorite_repo)

    @provide(scope=Scope.REQUEST)
    def provide_remove_from_favorites_uc(
        self, favorite_repo: IListingFavoriteRepository
    ) -> RemoveFromFavoritesUseCase:
        return RemoveFromFavoritesUseCase(favorite_repo)