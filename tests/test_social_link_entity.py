from uuid import uuid4

import pytest

from app.domain.entities.profile import PrivacyLevel
from app.domain.entities.social_link import SocialLink
from app.domain.value_objects.social_link import SocialPlatform


def create_link(**kwargs) -> SocialLink:
    defaults = {
        "profile_id": uuid4(),
        "platform": SocialPlatform.VK,
        "url": "https://vk.com/test",
    }
    defaults.update(kwargs)
    return SocialLink(**defaults)


def test_link_display_and_visibility():
    link = create_link()
    assert link.get_display_name().startswith("VK")
    dto = link.to_dto(viewer_role="USER", is_friend=True)
    assert dto["url"] == "https://vk.com/test"


def test_link_privacy():
    link = create_link(privacy_level=PrivacyLevel.PRIVATE)
    dto = link.to_dto(viewer_role="USER")
    assert dto["visible"] is False
    link.set_privacy(PrivacyLevel.PUBLIC)
    dto = link.to_dto(viewer_role="USER")
    assert dto["visible"] is True


@pytest.mark.parametrize(
    "platform,url",
    [
        (SocialPlatform.VK, "http://invalid"),
        (SocialPlatform.TELEGRAM, "tg://bad"),
        (SocialPlatform.WHATSAPP, "notphone"),
    ],
)
def test_link_invalid_url(platform, url):
    with pytest.raises(ValueError):
        create_link(platform=platform, url=url)


def test_update_and_verify():
    link = create_link()
    link.verify()
    assert link.is_verified is True
    link.unverify()
    assert link.is_verified is False
    with pytest.raises(ValueError):
        link.update_url("bad")