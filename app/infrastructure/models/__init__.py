# app/infrastructure/models/__init__.py

from advanced_alchemy.base import AdvancedDeclarativeBase

from .club_invitation import ClubInvitation
from .club_membership import ClubMembership
from .media_file import MediaFile
from .motoclub import MotoClub
from .motorcycle import Motorcycle
from .profile import Profile
from .social_link import SocialLink
from .user import User

# Для target_metadata в Alembic и единообразных импортов
Base = AdvancedDeclarativeBase()


__all__ = [
    "Base",
    "User",
    "Motorcycle",
    "SocialLink",
    "Profile",
    "MediaFile",
    "MotoClub",
    "ClubMembership",
    "ClubInvitation",
]
