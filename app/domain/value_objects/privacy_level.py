from enum import Enum


class PrivacyLevel(Enum):
    """Уровни приватности профиля"""
    PUBLIC = "public"
    FRIENDS_ONLY = "friends_only"
    MOTO_CLUB_MEMBERS = "moto_club_members"
    PRIVATE = "private"
