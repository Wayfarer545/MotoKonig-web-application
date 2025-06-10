# app/infrastructure/di/providers/use_cases/provider.py
"""Aggregates use case providers for different domains."""

from dishka import Provider

from .auth import AuthUseCaseProvider
from .club import ClubUseCaseProvider
from .listing import ListingUseCaseProvider
from .media import MediaUseCaseProvider
from .moto_club import MotoClubUseCaseProvider
from .motorcycle import MotorcycleUseCaseProvider
from .profile import ProfileUseCaseProvider
from .social_link import SocialLinkUseCaseProvider
from .user import UserUseCaseProvider


class UseCaseProvider(
    AuthUseCaseProvider,
    UserUseCaseProvider,
    MotorcycleUseCaseProvider,
    ProfileUseCaseProvider,
    SocialLinkUseCaseProvider,
    MediaUseCaseProvider,
    MotoClubUseCaseProvider,
    ClubUseCaseProvider,
    ListingUseCaseProvider,
    Provider,
):
    """Main provider that combines domain-specific providers."""

    pass
