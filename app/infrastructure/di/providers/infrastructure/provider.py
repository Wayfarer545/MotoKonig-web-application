# app/infrastructure/di/providers/infrastructure/provider.py
"""Aggregates infrastructure providers for repositories and services."""

from advanced_alchemy.extensions.fastapi import AdvancedAlchemy
from dishka import Provider

from app.config.settings import Config

from .base import InfrastructureBaseProvider
from .club import ClubRepoProvider
from .listing import ListingRepoProvider
from .media import MediaRepoProvider
from .moto_club import MotoClubRepoProvider
from .motorcycle import MotorcycleRepoProvider
from .profile import ProfileRepoProvider
from .services import ServicesProvider
from .social_link import SocialLinkRepoProvider
from .user import UserRepoProvider


class InfrastructureProvider(
    InfrastructureBaseProvider,
    UserRepoProvider,
    MotorcycleRepoProvider,
    ProfileRepoProvider,
    SocialLinkRepoProvider,
    MediaRepoProvider,
    MotoClubRepoProvider,
    ClubRepoProvider,
    ServicesProvider,
    ListingRepoProvider,
    Provider,
):
    def __init__(self, alchemy: AdvancedAlchemy, config: Config) -> None:
        InfrastructureBaseProvider.__init__(self, alchemy, config)
        ServicesProvider.__init__(self, config)
