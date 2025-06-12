from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from app.domain.entities.listing import Listing
from app.domain.value_objects.listing_category import ListingCategory
from app.domain.value_objects.listing_status import ListingStatus


def create_listing(**kwargs) -> Listing:
    defaults = {
        "seller_id": uuid4(),
        "title": "Продам мотоцикл",
        "description": "Очень хороший мотоцикл, полностью обслужен, сел и поехал.",
        "category": ListingCategory.MOTORCYCLES,
        "price": 100_000,
        "location": "Калининград",
    }
    defaults.update(kwargs)
    return Listing(**defaults)


def test_listing_creation_and_dto():
    listing = create_listing(contact_phone="+79001234567")
    assert listing.title == "Продам мотоцикл"
    assert listing.status == ListingStatus.DRAFT
    dto = listing.to_dto(include_private_info=True)
    assert dto["title"] == "Продам мотоцикл"
    assert dto["contact_phone"] == "+79001234567"


def test_listing_validation_errors():
    with pytest.raises(ValueError):
        create_listing(title="a")
    with pytest.raises(ValueError):
        create_listing(description="short desc")
    with pytest.raises(ValueError):
        create_listing(price=-1)
    with pytest.raises(ValueError):
        create_listing(location="")
    with pytest.raises(ValueError):
        create_listing(contact_phone="123")
    with pytest.raises(ValueError):
        create_listing(photo_urls=["1"] * 6)


def test_listing_status_flow():
    listing = create_listing()
    listing.submit_for_moderation()
    assert listing.status == ListingStatus.MODERATION
    listing.approve()
    assert listing.status == ListingStatus.ACTIVE
    listing.mark_as_sold()
    assert listing.status == ListingStatus.SOLD


def test_listing_expiry_and_visibility():
    listing = create_listing(status=ListingStatus.ACTIVE,
                             expires_at=datetime.utcnow() - timedelta(days=1))
    assert listing.is_expired() is True
    assert listing.is_visible_to_public() is False
    listing.extend_expiry(10)
    assert listing.is_expired() is False
    assert listing.status == ListingStatus.ACTIVE
