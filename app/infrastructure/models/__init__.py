# app/infrastructure/models/__init__.py

from advanced_alchemy.base import AdvancedDeclarativeBase

from .club_invitation import ClubInvitation
from .club_membership import ClubMembership
from .event import Event
from .event_participation import EventParticipation
from .listing import Listing
from .listing_favorite import ListingFavorite
from .media_file import MediaFile
from .motoclub import MotoClub
from .motokonig import MotoKonig
from .motokonig_achievement import MotoKonigAchievement
from .motorcycle import Motorcycle
from .profile import Profile
from .ride import Ride
from .ride_checkpoint import RideCheckpoint
from .ride_participant import RideParticipant
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
    "Listing",
    "ListingFavorite",
    "Event",
    "EventParticipation",
    "MotoKonig",
    "MotoKonigAchievement",
    "Ride",
    "RideParticipant",
    "RideCheckpoint",
]
