# tests/factories/profile_factory.py
from datetime import date, timedelta
from uuid import uuid4

from app.domain.entities.profile import Profile
from app.domain.value_objects.privacy_level import PrivacyLevel


class ProfileFactory:
    """Фабрика для создания профилей в тестах"""

    @staticmethod
    def create(**kwargs) -> Profile:
        defaults = {
            "user_id": uuid4(),
            "bio": "Тестовая биография пользователя",
            "location": "Калининград",
            "phone": "+79001234567",
            "date_of_birth": date.today() - timedelta(days=365*25),  # 25 лет
            "riding_experience": 5,
            "privacy_level": PrivacyLevel.PUBLIC,
        }
        defaults.update(kwargs)
        return Profile(**defaults)

    @staticmethod
    def create_private(**kwargs) -> Profile:
        kwargs.setdefault("privacy_level", PrivacyLevel.PRIVATE)
        return ProfileFactory.create(**kwargs)

    @staticmethod
    def create_young_rider(**kwargs) -> Profile:
        kwargs.setdefault("date_of_birth", date.today() - timedelta(days=365*18))
        kwargs.setdefault("riding_experience", 1)
        return ProfileFactory.create(**kwargs)
