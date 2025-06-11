from uuid import uuid4

from app.domain.entities.listing_favorite import ListingFavorite


def test_listing_favorite_dto():
    fav = ListingFavorite(user_id=uuid4(), listing_id=uuid4())
    dto = fav.to_dto()
    assert dto["user_id"] == fav.user_id
    assert dto["listing_id"] == fav.listing_id