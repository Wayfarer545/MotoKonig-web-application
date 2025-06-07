# app/infrastructure/repositories/sql_profile_repo.py

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.profile import PrivacyLevel, Profile
from app.domain.ports.repositories.profile import IProfileRepository
from app.domain.ports.specs.profile import ProfileSpecificationPort
from app.infrastructure.models.profile import Profile as ProfileModel


class SqlProfileRepository(IProfileRepository):
    """SQLAlchemy реализация репозитория профилей"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, profile: Profile) -> Profile:
        """Добавить новый профиль"""
        db_profile = ProfileModel(
            user_id=profile.user_id,
            bio=profile.bio,
            location=profile.location,
            phone=profile.phone,
            date_of_birth=profile.date_of_birth,
            riding_experience=profile.riding_experience,
            avatar_url=profile.avatar_url,
            privacy_level=profile.privacy_level,
            phone_privacy=profile.phone_privacy,
            location_privacy=profile.location_privacy,
        )

        self.session.add(db_profile)
        await self.session.flush()
        await self.session.refresh(db_profile)

        # Обновляем доменную сущность
        profile.id = db_profile.id
        profile.created_at = db_profile.created_at
        profile.updated_at = db_profile.updated_at

        return profile

    async def get(self, spec: ProfileSpecificationPort) -> Profile | None:
        """Получить профиль по спецификации"""
        statement = spec.to_query(
            select(ProfileModel).options(selectinload(ProfileModel.social_links))
        )
        result = await self.session.execute(statement)
        db_profile = result.scalar_one_or_none()

        if db_profile:
            return self._to_domain_entity(db_profile)
        return None

    async def get_list(self, spec: ProfileSpecificationPort | None = None) -> list[Profile]:
        """Получить список профилей по спецификации"""
        statement = select(ProfileModel).options(selectinload(ProfileModel.social_links))

        if spec:
            statement = spec.to_query(statement)

        result = await self.session.execute(statement)
        profiles = result.scalars().all()

        return [self._to_domain_entity(p) for p in profiles]

    async def update(self, profile: Profile) -> Profile:
        """Обновить профиль"""
        db_profile = await self.session.get(ProfileModel, profile.id)

        if db_profile:
            # Обновляем поля
            db_profile.bio = profile.bio
            db_profile.location = profile.location
            db_profile.phone = profile.phone
            db_profile.date_of_birth = profile.date_of_birth
            db_profile.riding_experience = profile.riding_experience
            db_profile.avatar_url = profile.avatar_url
            db_profile.privacy_level = profile.privacy_level
            db_profile.phone_privacy = profile.phone_privacy
            db_profile.location_privacy = profile.location_privacy

            await self.session.flush()
            await self.session.refresh(db_profile)

            # Обновляем timestamp в доменной сущности
            profile.updated_at = db_profile.updated_at

        return profile

    async def delete(self, profile_id: UUID) -> bool:
        """Удалить профиль"""
        db_profile = await self.session.get(ProfileModel, profile_id)

        if db_profile:
            await self.session.delete(db_profile)
            await self.session.flush()
            return True

        return False

    def _to_domain_entity(self, db_profile: ProfileModel) -> Profile:
        """Преобразовать модель БД в доменную сущность"""
        return Profile(
            profile_id=db_profile.id,
            user_id=db_profile.user_id,
            bio=db_profile.bio,
            location=db_profile.location,
            phone=db_profile.phone,
            date_of_birth=db_profile.date_of_birth,
            riding_experience=db_profile.riding_experience,
            avatar_url=db_profile.avatar_url,
            privacy_level=PrivacyLevel(db_profile.privacy_level.value),
            phone_privacy=PrivacyLevel(db_profile.phone_privacy.value),
            location_privacy=PrivacyLevel(db_profile.location_privacy.value),
            created_at=db_profile.created_at,
            updated_at=db_profile.updated_at
        )

