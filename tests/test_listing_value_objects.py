from app.domain.value_objects.listing_category import ListingCategory
from app.domain.value_objects.listing_status import ListingStatus


def test_listing_category_names():
    assert ListingCategory.MOTORCYCLES.get_display_name() == "Мотоциклы"
    assert "мотоциклов" in ListingCategory.MOTORCYCLES.get_description()


def test_listing_status_helpers():
    assert ListingStatus.ACTIVE.is_visible_to_public() is True
    assert ListingStatus.DRAFT.is_editable() is True
    assert ListingStatus.REJECTED.can_be_activated() is True