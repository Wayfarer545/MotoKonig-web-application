# app/domain/entities/social_link.py

from __future__ import annotations

import re
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.domain.entities.profile import PrivacyLevel
from app.domain.value_objects.social_link import SocialPlatform

if TYPE_CHECKING:
    pass


class SocialLink:
    """
    Доменная сущность социальной ссылки

    Инварианты:
    - URL должен соответствовать формату платформы
    - Каждая платформа может быть только одна у пользователя
    """

    def __init__(
            self,
            *,
            link_id: UUID | None = None,
            profile_id: UUID,
            platform: SocialPlatform,
            url: str,
            privacy_level: PrivacyLevel = PrivacyLevel.FRIENDS_ONLY,
            is_verified: bool = False,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ):
        # Валидация инвариантов
        self._validate_url_for_platform(platform, url)

        self.id: UUID = link_id or uuid4()
        self.profile_id: UUID = profile_id
        self.platform: SocialPlatform = platform
        self.url: str = url.strip()
        self.privacy_level: PrivacyLevel = privacy_level
        self.is_verified: bool = is_verified
        self.created_at: datetime | None = created_at
        self.updated_at: datetime | None = updated_at

    def _validate_url_for_platform(self, platform: SocialPlatform, url: str) -> None:
        """Валидация URL для конкретной платформы"""
        url = url.strip()

        patterns = {
            SocialPlatform.VK: r'^https?://(www\.)?vk\.com/[a-zA-Z0-9_.]+$',
            SocialPlatform.TELEGRAM: r'^(https?://(www\.)?t\.me/|@)[a-zA-Z0-9_]+$',
            SocialPlatform.WHATSAPP: r'^\+?[1-9]\d{6,14}$',  # Номер телефона
            SocialPlatform.INSTAGRAM: r'^https?://(www\.)?instagram\.com/[a-zA-Z0-9_.]+/?$',
            SocialPlatform.FACEBOOK: r'^https?://(www\.)?facebook\.com/[a-zA-Z0-9_.]+/?$',
            SocialPlatform.YOUTUBE: r'^https?://(www\.)?youtube\.com/(c/|channel/|user/|@)[a-zA-Z0-9_.-]+/?$',
        }

        pattern = patterns.get(platform)
        if pattern and not re.match(pattern, url):
            raise ValueError(f"Invalid {platform.value} URL format: {url}")

    def update_url(self, url: str) -> None:
        """Обновить URL"""
        self._validate_url_for_platform(self.platform, url)
        self.url = url.strip()

    def set_privacy(self, privacy_level: PrivacyLevel) -> None:
        """Установить уровень приватности"""
        self.privacy_level = privacy_level

    def verify(self) -> None:
        """Пометить ссылку как верифицированную"""
        self.is_verified = True

    def unverify(self) -> None:
        """Снять верификацию"""
        self.is_verified = False

    def is_visible_for(self, viewer_role: str, is_friend: bool = False, is_club_member: bool = False) -> bool:
        """Проверить, видна ли ссылка для определенного пользователя"""
        if self.privacy_level == PrivacyLevel.PUBLIC:
            return True
        elif self.privacy_level == PrivacyLevel.FRIENDS_ONLY:
            return is_friend
        elif self.privacy_level == PrivacyLevel.MOTO_CLUB_MEMBERS:
            return is_club_member
        elif self.privacy_level == PrivacyLevel.PRIVATE:
            return False
        return True

    def get_display_name(self) -> str:
        """Получить отображаемое имя для ссылки"""
        if self.platform == SocialPlatform.VK:
            # Извлекаем username из VK URL
            match = re.search(r'vk\.com/([a-zA-Z0-9_.]+)', self.url)
            return f"VK: {match.group(1)}" if match else "VK"
        elif self.platform == SocialPlatform.TELEGRAM:
            # Для Telegram может быть @username или t.me/username
            if self.url.startswith('@'):
                return f"Telegram: {self.url}"
            else:
                match = re.search(r't\.me/([a-zA-Z0-9_]+)', self.url)
                return f"Telegram: @{match.group(1)}" if match else "Telegram"
        elif self.platform == SocialPlatform.WHATSAPP:
            return f"WhatsApp: {self.url}"
        else:
            return f"{self.platform.value.title()}"

    def to_dto(self, viewer_role: str = "USER", is_friend: bool = False, is_club_member: bool = False) -> dict:
        """Конвертировать в DTO для API с учетом приватности"""
        if not self.is_visible_for(viewer_role, is_friend, is_club_member):
            return {
                "platform": self.platform.value,
                "display_name": self.platform.value.title(),
                "privacy_level": self.privacy_level.value,
                "visible": False
            }

        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "platform": self.platform.value,
            "url": self.url,
            "display_name": self.get_display_name(),
            "privacy_level": self.privacy_level.value,
            "is_verified": self.is_verified,
            "visible": True,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }