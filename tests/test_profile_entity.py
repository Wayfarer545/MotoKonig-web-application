from datetime import date, timedelta
from uuid import uuid4

import pytest

from app.domain.entities.profile import Profile
from app.domain.value_objects.privacy_level import PrivacyLevel


def create_profile(**kwargs) -> Profile:
    defaults = {
        "user_id": uuid4(),
        "bio": "hello",
        "location": "City",
        "phone": "+1234567890",
        "date_of_birth": date.today() - timedelta(days=365*20),
        "riding_experience": 5,
    }
    defaults.update(kwargs)
    return Profile(**defaults)


def test_profile_basic_and_age():
    profile = create_profile()
    assert profile.get_age() == 20
    dto = profile.to_dto(viewer_role="USER", is_friend=True)
    assert dto["bio"] == "hello"
    assert dto["phone"] == "+1234567890"


def test_profile_privacy_rules():
    profile = create_profile(privacy_level=PrivacyLevel.PRIVATE)
    dto = profile.to_dto(viewer_role="USER")
    assert dto["message"] == "Profile is private"
    profile.set_privacy_level(PrivacyLevel.PUBLIC)
    dto = profile.to_dto(viewer_role="USER")
    assert dto["bio"] == "hello"


@pytest.mark.parametrize(
    "field,value",
    [
        ("bio", "x" * 1001),
        ("phone", "1234"),
        ("date_of_birth", date.today() + timedelta(days=1)),
        ("date_of_birth", date.today() - timedelta(days=365*10)),
        ("riding_experience", -1),
        ("riding_experience", 100),
        ("location", "x" * 201),
    ],
)
def test_profile_invalid_values(field, value):
    with pytest.raises(ValueError):
        create_profile(**{field: value})


def test_profile_update_validation():
    profile = create_profile()
    with pytest.raises(ValueError):
        profile.update_bio("x" * 1001)
    with pytest.raises(ValueError):
        profile.update_phone("bad")
    with pytest.raises(ValueError):
        profile.update_location("y" * 201)