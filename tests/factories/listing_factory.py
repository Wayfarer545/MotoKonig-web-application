# tests/factories/listing_factory.py
from datetime import datetime, timedelta
from uuid import uuid4

from app.domain.entities.listing import Listing
from app.domain.value_objects.listing_category import ListingCategory
from app.domain.value_objects.listing_status import ListingStatus


class ListingFactory:
    """Фабрика для создания объявлений в тестах"""

    @staticmethod
    def create(**kwargs) -> Listing:
        defaults = {
            "seller_id": uuid4(),
            "title": "Продам отличный мотоцикл",
            "description": "Очень хороший мотоцикл в отличном состоянии, полностью обслужен",
            "category": ListingCategory.MOTORCYCLES,
            "price": 250_000,
            "location": "Калининград",
            "contact_phone": "+79001234567",
        }
        defaults.update(kwargs)
        return Listing(**defaults)

    @staticmethod
    def create_active(**kwargs) -> Listing:
        kwargs.setdefault("status", ListingStatus.ACTIVE)
        kwargs.setdefault("expires_at", datetime.utcnow() + timedelta(days=30))
        return ListingFactory.create(**kwargs)

    @staticmethod
    def create_expired(**kwargs) -> Listing:
        kwargs.setdefault("status", ListingStatus.ACTIVE)
        kwargs.setdefault("expires_at", datetime.utcnow() - timedelta(days=1))
        return ListingFactory.create(**kwargs)
