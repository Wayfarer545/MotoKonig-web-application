# app/infrastructure/repositories/sql_listing_category_repo.py

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.listing_category import ListingCategory
from domain.ports.repositories.listing_category_repository import IListingCategoryRepository
from app.domain.ports.specs.listing_category_specification import ListingCategorySpecificationPort
from app.infrastructure.models.listing_category_model import ListingCategory as ListingCategoryModel


class SqlListingCategoryRepository(IListingCategoryRepository):
    """SQLAlchemy реализация репозитория категорий объявлений"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, category: ListingCategory) -> ListingCategory:
        """Добавить новую категорию"""
        db_category = ListingCategoryModel(
            name=category.name,
            slug=category.slug,
            description=category.description,
            parent_id=category.parent_id,
            icon=category.icon,
            sort_order=category.sort_order,
            is_active=category.is_active,
        )

        self.session.add(db_category)
        await self.session.flush()
        await self.session.refresh(db_category)

        # Обновляем доменную сущность
        category.id = db_category.id
        category.created_at = db_category.created_at
        category.updated_at = db_category.updated_at

        return category

    async def get(self, spec: ListingCategorySpecificationPort) -> ListingCategory | None:
        """Получить категорию по спецификации"""
        statement = spec.to_query(select(ListingCategoryModel))
        result = await self.session.execute(statement)
        db_category = result.scalar_one_or_none()

        if db_category:
            return self._to_domain_entity(db_category)
        return None

    async def get_list(self, spec: ListingCategorySpecificationPort | None = None) -> list[ListingCategory]:
        """Получить список категорий по спецификации"""
        statement = select(ListingCategoryModel).order_by(
            ListingCategoryModel.sort_order,
            ListingCategoryModel.name
        )

        if spec:
            statement = spec.to_query(statement)

        result = await self.session.execute(statement)
        categories = result.scalars().all()

        return [self._to_domain_entity(category) for category in categories]

    async def update(self, category: ListingCategory) -> ListingCategory:
        """Обновить категорию"""
        db_category = await self.session.get(ListingCategoryModel, category.id)

        if db_category:
            # Обновляем поля
            db_category.name = category.name
            db_category.slug = category.slug
            db_category.description = category.description
            db_category.parent_id = category.parent_id
            db_category.icon = category.icon
            db_category.sort_order = category.sort_order
            db_category.is_active = category.is_active

            await self.session.flush()
            await self.session.refresh(db_category)

            # Обновляем timestamp в доменной сущности
            category.updated_at = db_category.updated_at

        return category

    async def delete(self, category_id: UUID) -> bool:
        """Удалить категорию"""
        db_category = await self.session.get(ListingCategoryModel, category_id)

        if db_category:
            await self.session.delete(db_category)
            await self.session.flush()
            return True

        return False

    async def get_root_categories(self) -> list[ListingCategory]:
        """Получить корневые категории"""
        statement = (
            select(ListingCategoryModel)
            .where(
                ListingCategoryModel.parent_id.is_(None),
                ListingCategoryModel.is_active == True
            )
            .order_by(ListingCategoryModel.sort_order, ListingCategoryModel.name)
        )

        result = await self.session.execute(statement)
        categories = result.scalars().all()

        return [self._to_domain_entity(category) for category in categories]

    async def get_subcategories(self, parent_id: UUID) -> list[ListingCategory]:
        """Получить подкатегории"""
        statement = (
            select(ListingCategoryModel)
            .where(
                ListingCategoryModel.parent_id == parent_id,
                ListingCategoryModel.is_active == True
            )
            .order_by(ListingCategoryModel.sort_order, ListingCategoryModel.name)
        )

        result = await self.session.execute(statement)
        categories = result.scalars().all()

        return [self._to_domain_entity(category) for category in categories]

    async def check_slug_exists(self, slug: str, exclude_id: UUID | None = None) -> bool:
        """Проверить существование slug"""
        statement = select(ListingCategoryModel).where(ListingCategoryModel.slug == slug)

        if exclude_id:
            statement = statement.where(ListingCategoryModel.id != exclude_id)

        result = await self.session.execute(statement)
        return result.scalar_one_or_none() is not None

    def _to_domain_entity(self, db_category: ListingCategoryModel) -> ListingCategory:
        """Преобразовать модель БД в доменную сущность"""
        return ListingCategory(
            category_id=db_category.id,
            name=db_category.name,
            slug=db_category.slug,
            description=db_category.description,
            parent_id=db_category.parent_id,
            icon=db_category.icon,
            sort_order=db_category.sort_order,
            is_active=db_category.is_active,
            created_at=db_category.created_at,
            updated_at=db_category.updated_at
        )