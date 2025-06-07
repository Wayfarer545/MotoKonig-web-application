# app/infrastructure/repositories/sql_listing_repo.py

from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.listing import Listing
from domain.ports.repositories.listing_repository import IListingRepository
from domain.ports.specs.listing import ListingSpecificationPort
from app.domain.value_objects.listing_status import ListingStatus
from app.domain.value_objects.listing_type import ListingType
from app.infrastructure.models.listing_model import Listing as ListingModel


class SqlListingRepository(IListingRepository):
    """SQLAlchemy реализация репозитория объявлений"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, listing: Listing) -> Listing:
        """Добавить новое объявление"""
        db_listing = ListingModel(
            seller_id=listing.seller_id,
            category_id=listing.category_id,
            title=listing.title,
            description=listing.description,
            price=float(listing.price),
            listing_type=listing.listing_type,
            status=listing.status,
            location=listing.location,
            latitude=float(listing.latitude) if listing.latitude else None,
            longitude=float(listing.longitude) if listing.longitude else None,
            contact_phone=listing.contact_phone,
            contact_email=listing.contact_email,
            is_negotiable=listing.is_negotiable,
            condition=listing.condition,
            brand=listing.brand,
            model=listing.model,
            year=listing.year,
            mileage=listing.mileage,
            is_featured=listing.is_featured,
            views_count=listing.views_count,
            favorites_count=listing.favorites_count,
            expires_at=listing.expires_at.isoformat() if listing.expires_at else None,
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
        statement = spec.to_query(
            select(ListingModel).options(
                selectinload(ListingModel.images),
                selectinload(ListingModel.category)
            )
        )
        result = await self.session.execute(statement)
        db_listing = result.scalar_one_or_none()

        if db_listing:
            return self._to_domain_entity(db_listing)
        return None

    async def get_list(self, spec: ListingSpecificationPort | None = None) -> list[Listing]:
        """Получить список объявлений по спецификации"""
        statement = select(ListingModel).options(
            selectinload(ListingModel.images),
            selectinload(ListingModel.category)
        )

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
            db_listing.price = float(listing.price)
            db_listing.listing_type = listing.listing_type
            db_listing.status = listing.status
            db_listing.location = listing.location
            db_listing.latitude = float(listing.latitude) if listing.latitude else None
            db_listing.longitude = float(listing.longitude) if listing.longitude else None
            db_listing.contact_phone = listing.contact_phone
            db_listing.contact_email = listing.contact_email
            db_listing.is_negotiable = listing.is_negotiable
            db_listing.condition = listing.condition
            db_listing.brand = listing.brand
            db_listing.model = listing.model
            db_listing.year = listing.year
            db_listing.mileage = listing.mileage
            db_listing.is_featured = listing.is_featured
            db_listing.views_count = listing.views_count
            db_listing.favorites_count = listing.favorites_count
            db_listing.expires_at = listing.expires_at.isoformat() if listing.expires_at else None

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

    async def increment_views(self, listing_id: UUID) -> None:
        """Увеличить счетчик просмотров"""
        statement = (
            update(ListingModel)
            .where(ListingModel.id == listing_id)
            .values(views_count=ListingModel.views_count + 1)
        )
        await self.session.execute(statement)
        await self.session.flush()

    async def get_featured_listings(self, limit: int = 10) -> list[Listing]:
        """Получить рекомендуемые объявления"""
        statement = (
            select(ListingModel)
            .options(
                selectinload(ListingModel.images),
                selectinload(ListingModel.category)
            )
            .where(
                ListingModel.status == ListingStatus.FEATURED,
                ListingModel.is_featured == True
            )
            .order_by(ListingModel.created_at.desc())
            .limit(limit)
        )

        result = await self.session.execute(statement)
        listings = result.scalars().all()

        return [self._to_domain_entity(listing) for listing in listings]

    def _to_domain_entity(self, db_listing: ListingModel) -> Listing:
        """Преобразовать модель БД в доменную сущность"""
        from datetime import datetime
        from decimal import Decimal

        expires_at = None
        if db_listing.expires_at:
            try:
                expires_at = datetime.fromisoformat(db_listing.expires_at)
            except ValueError:
                expires_at = None

        return Listing(
            listing_id=db_listing.id,
            seller_id=db_listing.seller_id,
            category_id=db_listing.category_id,
            title=db_listing.title,
            description=db_listing.description,
            price=Decimal(str(db_listing.price)),
            listing_type=ListingType(db_listing.listing_type.value),
            status=ListingStatus(db_listing.status.value),
            location=db_listing.location,
            latitude=float(db_listing.latitude) if db_listing.latitude else None,
            longitude=float(db_listing.longitude) if db_listing.longitude else None,
            contact_phone=db_listing.contact_phone,
            contact_email=db_listing.contact_email,
            is_negotiable=db_listing.is_negotiable,
            condition=db_listing.condition,
            brand=db_listing.brand,
            model=db_listing.model,
            year=db_listing.year,
            mileage=db_listing.mileage,
            is_featured=db_listing.is_featured,
            views_count=db_listing.views_count,
            favorites_count=db_listing.favorites_count,
            expires_at=expires_at,
            created_at=db_listing.created_at,
            updated_at=db_listing.updated_at
        )