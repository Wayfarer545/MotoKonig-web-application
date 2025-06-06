# app/domain/entities/profile.py

from __future__ import annotations

import re
from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.domain.value_objects.privacy_level import PrivacyLevel

if TYPE_CHECKING:
    pass


class Profile:
    """
    Доменная сущность профиля пользователя

    Инварианты:
    - Телефон должен соответствовать формату
    - Дата рождения не может быть в будущем
    - Опыт вождения не может быть отрицательным
    - Bio не может быть слишком длинным
    """

    def __init__(
            self,
            *,
            profile_id: UUID | None = None,
            user_id: UUID,
            bio: str | None = None,
            location: str | None = None,
            phone: str | None = None,
            date_of_birth: date | None = None,
            riding_experience: int | None = None,  # в годах
            avatar_url: str | None = None,
            privacy_level: PrivacyLevel = PrivacyLevel.PUBLIC,
            phone_privacy: PrivacyLevel = PrivacyLevel.FRIENDS_ONLY,
            location_privacy: PrivacyLevel = PrivacyLevel.PUBLIC,
            created_at: datetime | None = None,
            updated_at: datetime | None = None,
    ):
        # Валидация инвариантов
        if bio is not None:
            self._validate_bio(bio)
        if phone is not None:
            self._validate_phone(phone)
        if date_of_birth is not None:
            self._validate_date_of_birth(date_of_birth)
        if riding_experience is not None:
            self._validate_riding_experience(riding_experience)
        if location is not None:
            self._validate_location(location)

        self.id: UUID = profile_id or uuid4()
        self.user_id: UUID = user_id
        self.bio: str | None = bio.strip() if bio else None
        self.location: str | None = location.strip() if location else None
        self.phone: str | None = phone.strip() if phone else None
        self.date_of_birth: date | None = date_of_birth
        self.riding_experience: int | None = riding_experience
        self.avatar_url: str | None = avatar_url
        self.privacy_level: PrivacyLevel = privacy_level
        self.phone_privacy: PrivacyLevel = phone_privacy
        self.location_privacy: PrivacyLevel = location_privacy
        self.created_at: datetime | None = created_at
        self.updated_at: datetime | None = updated_at

    def _validate_bio(self, bio: str) -> None:
        """Валидация биографии"""
        if len(bio.strip()) > 1000:
            raise ValueError("Bio cannot be longer than 1000 characters")

    def _validate_phone(self, phone: str) -> None:
        """Валидация телефона"""
        # Простая валидация для международных номеров
        phone_pattern = r'^\+?[1-9]\d{6,14}$'
        if not re.match(phone_pattern, phone.replace(' ', '').replace('-', '')):
            raise ValueError("Invalid phone number format")

    def _validate_date_of_birth(self, birth_date: date) -> None:
        """Валидация даты рождения"""
        if birth_date >= date.today():
            raise ValueError("Date of birth cannot be in the future")

        # Проверяем минимальный возраст (например, 16 лет)
        age = (date.today() - birth_date).days // 365
        if age < 16:
            raise ValueError("User must be at least 16 years old")

    def _validate_riding_experience(self, experience: int) -> None:
        """Валидация опыта вождения"""
        if experience < 0:
            raise ValueError("Riding experience cannot be negative")
        if experience > 80:
            raise ValueError("Riding experience seems unrealistic")

    def _validate_location(self, location: str) -> None:
        """Валидация локации"""
        if len(location.strip()) > 200:
            raise ValueError("Location cannot be longer than 200 characters")

    def update_bio(self, bio: str | None) -> None:
        """Обновить биографию"""
        if bio is not None:
            self._validate_bio(bio)
        self.bio = bio.strip() if bio else None

    def update_phone(self, phone: str | None) -> None:
        """Обновить телефон"""
        if phone is not None:
            self._validate_phone(phone)
        self.phone = phone.strip() if phone else None

    def update_location(self, location: str | None) -> None:
        """Обновить локацию"""
        if location is not None:
            self._validate_location(location)
        self.location = location.strip() if location else None

    def set_privacy_level(self, privacy_level: PrivacyLevel) -> None:
        """Установить общий уровень приватности"""
        self.privacy_level = privacy_level

    def set_phone_privacy(self, privacy_level: PrivacyLevel) -> None:
        """Установить приватность телефона"""
        self.phone_privacy = privacy_level

    def set_location_privacy(self, privacy_level: PrivacyLevel) -> None:
        """Установить приватность локации"""
        self.location_privacy = privacy_level

    def update_avatar(self, avatar_url: str | None) -> None:
        """Обновить аватар"""
        self.avatar_url = avatar_url

    def get_age(self) -> int | None:
        """Получить возраст пользователя"""
        if not self.date_of_birth:
            return None
        return (date.today() - self.date_of_birth).days // 365

    def is_profile_visible_for(self, viewer_role: str, is_friend: bool = False, is_club_member: bool = False) -> bool:
        """Проверить, виден ли профиль для определенного пользователя"""
        if self.privacy_level == PrivacyLevel.PUBLIC:
            return True
        elif self.privacy_level == PrivacyLevel.FRIENDS_ONLY:
            return is_friend
        elif self.privacy_level == PrivacyLevel.MOTO_CLUB_MEMBERS:
            return is_club_member
        elif self.privacy_level == PrivacyLevel.PRIVATE:
            return False
        return True

    def is_phone_visible_for(self, viewer_role: str, is_friend: bool = False, is_club_member: bool = False) -> bool:
        """Проверить, виден ли телефон для определенного пользователя"""
        if self.phone_privacy == PrivacyLevel.PUBLIC:
            return True
        elif self.phone_privacy == PrivacyLevel.FRIENDS_ONLY:
            return is_friend
        elif self.phone_privacy == PrivacyLevel.MOTO_CLUB_MEMBERS:
            return is_club_member
        elif self.phone_privacy == PrivacyLevel.PRIVATE:
            return False
        return True

    def to_dto(self, viewer_role: str = "USER", is_friend: bool = False, is_club_member: bool = False) -> dict:
        """Конвертировать в DTO для API с учетом приватности"""
        if not self.is_profile_visible_for(viewer_role, is_friend, is_club_member):
            return {
                "id": self.id,
                "user_id": self.user_id,
                "privacy_level": self.privacy_level.value,
                "message": "Profile is private"
            }

        dto = {
            "id": self.id,
            "user_id": self.user_id,
            "bio": self.bio,
            "location": self.location,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "age": self.get_age(),
            "riding_experience": self.riding_experience,
            "avatar_url": self.avatar_url,
            "privacy_level": self.privacy_level.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

        # Телефон показываем только при соответствующих правах
        if self.is_phone_visible_for(viewer_role, is_friend, is_club_member):
            dto["phone"] = self.phone
        else:
            dto["phone"] = None

        return dto
