# app/infrastructure/repositories/sql_achievement_repo.py

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.achievement import Achievement
from app.domain.ports.repositories.achievement import IAchievementRepository
from app.domain.value_objects.achievement_type import AchievementType
from app.infrastructure.models.motokonig_achievement import (
    MotoKonigAchievement as AchievementModel,
)

__all__ = ["SqlAchievementRepository"]


class SqlAchievementRepository(IAchievementRepository):
    """SQL реализация репозитория достижений"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain_entity(self, db_model: AchievementModel) -> Achievement:
        """Преобразовать модель БД в доменную сущность"""
        return Achievement(
            achievement_id=db_model.id,
            achievement_type=db_model.achievement_type,
            earned_at=db_model.earned_at,
            description=db_model.description,
            metadata=db_model.achievement_metadata,
        )

    async def add(self, achievement: Achievement, motokonig_id: UUID) -> Achievement:
        """Добавить новое достижение"""
        db_model = AchievementModel(
            motokonig_id=str(motokonig_id),
            achievement_type=achievement.achievement_type,
            earned_at=achievement.earned_at,
            description=achievement.description,
            achievement_metadata=achievement.metadata,
        )

        self.session.add(db_model)
        await self.session.flush()
        await self.session.refresh(db_model)

        return self._to_domain_entity(db_model)

    async def get_by_motokonig(self, motokonig_id: UUID) -> list[Achievement]:
        """Получить все достижения профиля"""
        statement = select(AchievementModel).where(
            AchievementModel.motokonig_id == str(motokonig_id)
        )
        result = await self.session.execute(statement)
        db_models = result.scalars().all()

        return [self._to_domain_entity(model) for model in db_models]

    async def has_achievement(self, motokonig_id: UUID, achievement_type: AchievementType) -> bool:
        """Проверить наличие достижения у профиля"""
        statement = select(AchievementModel).where(
            AchievementModel.motokonig_id == str(motokonig_id),
            AchievementModel.achievement_type == achievement_type
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none() is not None

    async def get_achievement_stats(self) -> dict[AchievementType, int]:
        """Получить статистику по достижениям"""
        # TODO: Реализовать агрегацию
        return {}
