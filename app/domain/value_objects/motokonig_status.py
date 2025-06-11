# app/domain/value_objects/motokonig_status.py
from enum import StrEnum


class MotoKonigStatus(StrEnum):
    """Статус MotoKonig в иерархии"""
    NOVICE = "novice"
    RIDER = "rider"
    EXPERT = "expert"
    MASTER = "master"
    LEGEND = "legend"
    KONIG = "konig"  # Король дорог!
