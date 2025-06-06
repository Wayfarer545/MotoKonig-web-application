# app/infrastructure/models/__init__.py

from advanced_alchemy.base import AdvancedDeclarativeBase

from .club_invitation_model import ClubInvitation
from .club_membership_model import ClubMembership
from .media_file_model import MediaFile
from .moto_club_model import MotoClub
from .motorcycle_model import Motorcycle
from .profile_model import Profile
from .social_link_model import SocialLink
from .user_model import User

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
