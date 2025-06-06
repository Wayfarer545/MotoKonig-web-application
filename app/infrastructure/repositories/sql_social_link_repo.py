# app/infrastructure/repositories/sql_social_link_repo.py

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.social_link import SocialLink, SocialPlatform, PrivacyLevel
from app.domain.ports.social_link_repository import ISocialLinkRepository
from app.domain.ports.social_link_specification import SocialLinkSpecificationPort
from app.infrastructure.models.social_link_model import SocialLink as SocialLinkModel


class SqlSocialLinkRepository(ISocialLinkRepository):
    """SQLAlchemy реализация репозитория социальных ссылок"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, social_link: SocialLink) -> SocialLink:
        """Добавить новую социальную ссылку"""
        db_link = SocialLinkModel(
            profile_id=social_link.profile_id,
            platform=social_link.platform,
            url=social_link.url,
            privacy_level=social_link.privacy_level,
            is_verified=social_link.is_verified,
        )

        self.session.add(db_link)
        await self.session.flush()
        await self.session.refresh(db_link)

        # Обновляем доменную сущность
        social_link.id = db_link.id
        social_link.created_at = db_link.created_at
        social_link.updated_at = db_link.updated_at

        return social_link

    async def get(self, spec: SocialLinkSpecificationPort) -> SocialLink | None:
        """Получить социальную ссылку по спецификации"""
        statement = spec.to_query(select(SocialLinkModel))
        result = await self.session.execute(statement)
        db_link = result.scalar_one_or_none()

        if db_link:
            return self._to_domain_entity(db_link)
        return None

    async def get_list(self, spec: SocialLinkSpecificationPort | None = None) -> list[SocialLink]:
        """Получить список социальных ссылок по спецификации"""
        statement = select(SocialLinkModel)

        if spec:
            statement = spec.to_query(statement)

        result = await self.session.execute(statement)
        links = result.scalars().all()

        return [self._to_domain_entity(link) for link in links]

    async def update(self, social_link: SocialLink) -> SocialLink:
        """Обновить социальную ссылку"""
        db_link = await self.session.get(SocialLinkModel, social_link.id)

        if db_link:
            # Обновляем поля
            db_link.url = social_link.url
            db_link.privacy_level = social_link.privacy_level
            db_link.is_verified = social_link.is_verified

            await self.session.flush()
            await self.session.refresh(db_link)

            # Обновляем timestamp в доменной сущности
            social_link.updated_at = db_link.updated_at

        return social_link

    async def delete(self, link_id: UUID) -> bool:
        """Удалить социальную ссылку"""
        db_link = await self.session.get(SocialLinkModel, link_id)

        if db_link:
            await self.session.delete(db_link)
            await self.session.flush()
            return True

        return False

    async def delete_by_profile_and_platform(self, profile_id: UUID, platform: SocialPlatform) -> bool:
        """Удалить ссылку по профилю и платформе"""
        statement = select(SocialLinkModel).where(
            SocialLinkModel.profile_id == profile_id,
            SocialLinkModel.platform == platform
        )
        result = await self.session.execute(statement)
        db_link = result.scalar_one_or_none()

        if db_link:
            await self.session.delete(db_link)
            await self.session.flush()
            return True

        return False

    def _to_domain_entity(self, db_link: SocialLinkModel) -> SocialLink:
        """Преобразовать модель БД в доменную сущность"""
        return SocialLink(
            link_id=db_link.id,
            profile_id=db_link.profile_id,
            platform=SocialPlatform(db_link.platform.value),
            url=db_link.url,
            privacy_level=PrivacyLevel(db_link.privacy_level.value),
            is_verified=db_link.is_verified,
            created_at=db_link.created_at,
            updated_at=db_link.updated_at
        )