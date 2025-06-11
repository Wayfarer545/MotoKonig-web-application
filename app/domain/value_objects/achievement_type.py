# app/domain/value_objects/achievement_type.py
from enum import StrEnum


class AchievementType(StrEnum):
    """Типы достижений для MotoKonig"""
    FIRST_RIDE = "first_ride"
    DISTANCE_100K = "distance_100k"
    DISTANCE_1000K = "distance_1000k"
    SPEED_DEMON = "speed_demon"
    NIGHT_RIDER = "night_rider"
    RAIN_MASTER = "rain_master"
    TRACK_DAY = "track_day"
    CUSTOM_BUILD = "custom_build"
    GROUP_RIDE = "group_ride"
    MENTOR = "mentor"
