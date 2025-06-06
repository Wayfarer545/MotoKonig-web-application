# app/infrastructure/models/__init__.py

from advanced_alchemy.base import AdvancedDeclarativeBase

from .motorcycle_model import Motorcycle
from .user_model import User
from .social_link_model import SocialLink
from .profile_model import Profile


# Для target_metadata в Alembic и единообразных импортов
Base = AdvancedDeclarativeBase()


__all__ = [
    "Base",
    "User",
    "Motorcycle",
    "SocialLink",
    "Profile",
]
