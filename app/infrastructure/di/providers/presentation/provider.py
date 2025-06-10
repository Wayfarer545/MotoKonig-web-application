# app/infrastructure/di/providers/presentation/provider.py
"""Aggregates controller providers for different domains."""

from dishka import Provider

from .auth import AuthControllerProvider
from .listing import ListingControllerProvider
from .media import MediaControllerProvider
from .moto_club import MotoClubControllerProvider
from .motorcycle import MotorcycleControllerProvider
from .profile import ProfileControllerProvider
from .user import UserControllerProvider


class PresentationProvider(
    UserControllerProvider,
    MotorcycleControllerProvider,
    AuthControllerProvider,
    ProfileControllerProvider,
    MediaControllerProvider,
    ListingControllerProvider,
    MotoClubControllerProvider,

    Provider,
):
    """Main provider that combines domain-specific controller providers."""

    pass
