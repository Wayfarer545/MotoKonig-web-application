# app/infrastructure/di/providers/presentation/listing.py

from dishka import Provider, Scope, provide

from app.application.controllers.listing_controller import ListingController
from app.application.use_cases.listing.add_to_favorites import AddToFavoritesUseCase
from app.application.use_cases.listing.create_listing import CreateListingUseCase
from app.application.use_cases.listing.delete_listing import DeleteListingUseCase
from app.application.use_cases.listing.get_listing import GetListingUseCase
from app.application.use_cases.listing.list_listings import ListListingsUseCase
from app.application.use_cases.listing.remove_from_favorites import (
    RemoveFromFavoritesUseCase,
)
from app.application.use_cases.listing.update_listing import UpdateListingUseCase


class ListingControllerProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_listing_controller(
        self,
        create_uc: CreateListingUseCase,
        get_uc: GetListingUseCase,
        list_uc: ListListingsUseCase,
        update_uc: UpdateListingUseCase,
        delete_uc: DeleteListingUseCase,
        add_favorite_uc: AddToFavoritesUseCase,
        remove_favorite_uc: RemoveFromFavoritesUseCase,
    ) -> ListingController:
        return ListingController(
            create_uc,
            get_uc,
            list_uc,
            update_uc,
            delete_uc,
            add_favorite_uc,
            remove_favorite_uc,
        )
