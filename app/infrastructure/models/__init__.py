# app/infrastructure/models/__init__.py
from advanced_alchemy.base import AdvancedDeclarativeBase

from .user_model import User

# Для target_metadata в Alembic и единообразных импортов
Base = AdvancedDeclarativeBase()

__all__ = [
    "Base",
    "User",
]
