# app/infrastructure/repositories/sql_listing_repo.py

import json
from datetime import datetime
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.listing import Listing
from app.domain.ports.repositories.listing import IListingRepository
from app.domain.ports.specs.listing import ListingSpecificationPort
from app.domain.value_objects.listing_category import ListingCategory
from app.domain.value_objects.listing_status import ListingStatus
from app.infrastructure.models.listing import Listing as ListingModel


class SqlListingRepository(IListingRepository):
    """SQLAlchemy реализация репозитория объявлений"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, listing: Listing) -> Listing:
        """Добавить новое объявление"""
        db_listing = ListingModel(
            seller_id=listing.seller_id,
            title=listing.title,
            description=listing.description,
            category=listing.category,
            price=listing.price,
            currency=listing.currency,
            location=listing.location,
            status=listing.status,
            is_negotiable=listing.is_negotiable,
            contact_phone=listing.contact_phone,
            contact_email=listing.contact_email,
            photo_urls=json.dumps(listing.photo_urls) if listing.photo_urls else None,
            views_count=listing.views_count,
            expires_at=listing.expires_at.isoformat() if listing.expires_at else None,
            moderation_notes=listing.moderation_notes,
            is_featured=listing.is_featured,
        )

        self.session.add(db_listing)
        await self.session.flush()
        await self.session.refresh(db_listing)

        # Обновляем доменную сущность
        listing.id = db_listing.id
        listing.created_at = db_listing.created_at
        listing.updated_at = db_listing.updated_at

        return listing

    async def get(self, spec: ListingSpecificationPort) -> Listing | None:
        """Получить объявление по спецификации"""
        statement = spec.to_query(select(ListingModel))
        result = await self.session.execute(statement)
        db_listing = result.scalar_one_or_none()

        if db_listing:
            return self._to_domain_entity(db_listing)
        return None

    async def get_list(self, spec: ListingSpecificationPort | None = None) -> list[Listing]:
        """Получить список объявлений по спецификации"""
        statement = select(ListingModel)

        if spec:
            statement = spec.to_query(statement)

        result = await self.session.execute(statement)
        listings = result.scalars().all()

        return [self._to_domain_entity(listing) for listing in listings]

    async def update(self, listing: Listing) -> Listing:
        """Обновить объявление"""
        db_listing = await self.session.get(ListingModel, listing.id)

        if db_listing:
            # Обновляем поля
            db_listing.title = listing.title
            db_listing.description = listing.description
            db_listing.category = listing.category
            db_listing.price = listing.price
            db_listing.currency = listing.currency
            db_listing.location = listing.location
            db_listing.status = listing.status
            db_listing.is_negotiable = listing.is_negotiable
            db_listing.contact_phone = listing.contact_phone
            db_listing.contact_email = listing.contact_email
            db_listing.photo_urls = json.dumps(listing.photo_urls) if listing.photo_urls else None
            db_listing.views_count = listing.views_count
            db_listing.expires_at = listing.expires_at.isoformat() if listing.expires_at else None
            db_listing.moderation_notes = listing.moderation_notes
            db_listing.is_featured = listing.is_featured

            await self.session.flush()
            await self.session.refresh(db_listing)

            # Обновляем timestamp в доменной сущности
            listing.updated_at = db_listing.updated_at

        return listing

    async def delete(self, listing_id: UUID) -> bool:
        """Удалить объявление"""
        db_listing = await self.session.get(ListingModel, listing_id)

        if db_listing:
            await self.session.delete(db_listing)
            await self.session.flush()
            return True

        return False

    async def count_active_by_seller(self, seller_id: UUID) -> int:
        """Подсчитать активные объявления продавца"""
        statement = select(func.count(ListingModel.id)).where(
            ListingModel.seller_id == seller_id,
            ListingModel.status.in_([
                ListingStatus.DRAFT,
                ListingStatus.MODERATION,
                ListingStatus.ACTIVE,
                ListingStatus.SUSPENDED
            ])
        )
        result = await self.session.execute(statement)
        return result.scalar() or 0

    async def expire_old_listings(self) -> int:
        """Пометить старые объявления как истёкшие"""
        current_time = datetime.utcnow().isoformat()

        statement = (
            update(ListingModel)
            .where(
                ListingModel.status == ListingStatus.ACTIVE,
                ListingModel.expires_at < current_time
            )
            .values(status=ListingStatus.EXPIRED)
        )

        result = await self.session.execute(statement)
        await self.session.flush()

        return result.rowcount or 0

    def _to_domain_entity(self, db_listing: ListingModel) -> Listing:
        """Преобразовать модель БД в доменную сущность"""
        expires_at = None
        if db_listing.expires_at:
            try:
                expires_at = datetime.fromisoformat(db_listing.expires_at)
            except ValueError:
                expires_at = None

        photo_urls = []
        if db_listing.photo_urls:
            try:
                photo_urls = json.loads(db_listing.photo_urls)
            except (json.JSONDecodeError, TypeError):
                photo_urls = []

        return Listing(
            listing_id=db_listing.id,
            seller_id=db_listing.seller_id,
            title=db_listing.title,
            description=db_listing.description,
            category=ListingCategory(db_listing.category.value),
            price=db_listing.price,
            currency=db_listing.currency,
            location=db_listing.location,
            status=ListingStatus(db_listing.status.value),
            is_negotiable=db_listing.is_negotiable,
            contact_phone=db_listing.contact_phone,
            contact_email=db_listing.contact_email,
            photo_urls=photo_urls,
            views_count=db_listing.views_count,
            expires_at=expires_at,
            moderation_notes=db_listing.moderation_notes,
            is_featured=db_listing.is_featured,
            created_at=db_listing.created_at,
            updated_at=db_listing.updated_at
        )
