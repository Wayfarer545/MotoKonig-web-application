# app/infrastructure/repositories/sql_motokonig_repo.py

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.achievement import Achievement
from app.domain.entities.motokonig import MotoKonig
from app.domain.ports.repositories.motokonig import IMotoKonigRepository
from app.domain.ports.specs.motokonig import MotoKonigSpecificationPort
from app.infrastructure.models.motokonig import MotoKonig as MotoKonigModel
from app.infrastructure.models.motokonig_achievement import (
    MotoKonigAchievement as AchievementModel,
)

__all__ = ["SqlMotoKonigRepository"]


class SqlMotoKonigRepository(IMotoKonigRepository):
    """SQL реализация репозитория MotoKonig"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain_entity(self, db_model: MotoKonigModel) -> MotoKonig:
        """Преобразовать модель БД в доменную сущность"""
        achievements = [
            Achievement(
                achievement_id=a.id,
                achievement_type=a.achievement_type,
                earned_at=a.earned_at,
                description=a.description,
                metadata=a.achievement_metadata,
            )
            for a in db_model.achievements
        ]

        return MotoKonig(
            motokonig_id=UUID(db_model.id),
            user_id=UUID(db_model.user_id),
            nickname=db_model.nickname,
            status=db_model.status,
            experience_points=db_model.experience_points,
            total_distance=db_model.total_distance,
            total_rides=db_model.total_rides,
            average_speed=db_model.average_speed,
            max_speed=db_model.max_speed,
            rating=db_model.rating,
            bio=db_model.bio,
            avatar_url=db_model.avatar_url,
            is_public=db_model.is_public,
            achievements=achievements,
            created_at=db_model.created_at,
            updated_at=db_model.updated_at,
        )

    async def add(self, motokonig: MotoKonig) -> MotoKonig:
        """Добавить новый профиль"""
        db_model = MotoKonigModel(
            user_id=str(motokonig.user_id),
            nickname=motokonig.nickname,
            status=motokonig.status,
            experience_points=motokonig.experience_points,
            total_distance=motokonig.total_distance,
            total_rides=motokonig.total_rides,
            average_speed=motokonig.average_speed,
            max_speed=motokonig.max_speed,
            rating=motokonig.rating,
            bio=motokonig.bio,
            avatar_url=motokonig.avatar_url,
            is_public=motokonig.is_public,
        )

        self.session.add(db_model)
        await self.session.flush()
        await self.session.refresh(db_model)

        return self._to_domain_entity(db_model)

    async def get(self, spec: MotoKonigSpecificationPort) -> MotoKonig | None:
        """Получить профиль по спецификации"""
        statement = spec.to_query(select(MotoKonigModel))
        result = await self.session.execute(statement)
        db_model = result.scalar_one_or_none()

        if db_model:
            return self._to_domain_entity(db_model)
        return None

    async def get_by_id(self, motokonig_id: UUID) -> MotoKonig | None:
        """Получить профиль по ID"""
        from app.infrastructure.specs.motokonig.motokonig_by_id import MotoKonigById
        return await self.get(MotoKonigById(motokonig_id))

    async def get_by_user_id(self, user_id: UUID) -> MotoKonig | None:
        """Получить профиль по ID пользователя"""
        from app.infrastructure.specs.motokonig.motokonig_by_user_id import (
            MotoKonigByUserId,
        )
        return await self.get(MotoKonigByUserId(user_id))

    async def get_list(self, spec: MotoKonigSpecificationPort | None = None) -> list[MotoKonig]:
        """Получить список профилей"""
        statement = select(MotoKonigModel)

        if spec:
            statement = spec.to_query(statement)

        result = await self.session.execute(statement)
        db_models = result.scalars().all()

        return [self._to_domain_entity(model) for model in db_models]

    async def update(self, motokonig: MotoKonig) -> MotoKonig:
        """Обновить профиль"""
        db_model = await self.session.get(MotoKonigModel, str(motokonig.motokonig_id))

        if db_model:
            db_model.nickname = motokonig.nickname
            db_model.status = motokonig.status
            db_model.experience_points = motokonig.experience_points
            db_model.total_distance = motokonig.total_distance
            db_model.total_rides = motokonig.total_rides
            db_model.average_speed = motokonig.average_speed
            db_model.max_speed = motokonig.max_speed
            db_model.rating = motokonig.rating
            db_model.bio = motokonig.bio
            db_model.avatar_url = motokonig.avatar_url
            db_model.is_public = motokonig.is_public

            # Обновляем достижения
            for achievement in motokonig.achievements:
                if not any(a.achievement_type == achievement.achievement_type for a in db_model.achievements):
                    db_achievement = AchievementModel(
                        motokonig_id=db_model.id,
                        achievement_type=achievement.achievement_type,
                        earned_at=achievement.earned_at,
                        description=achievement.description,
                        metadata=achievement.achievement_metadata,
                    )
                    self.session.add(db_achievement)

            await self.session.flush()
            await self.session.refresh(db_model)

        return self._to_domain_entity(db_model)

    async def delete(self, motokonig_id: UUID) -> None:
        """Удалить профиль"""
        db_model = await self.session.get(MotoKonigModel, str(motokonig_id))
        if db_model:
            await self.session.delete(db_model)
            await self.session.flush()

    async def exists(self, spec: MotoKonigSpecificationPort) -> bool:
        """Проверить существование профиля"""
        model = await self.get(spec)
        return model is not None
