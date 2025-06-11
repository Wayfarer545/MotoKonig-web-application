# app/application/use_cases/motokonig/create_profile.py

from uuid import UUID

from app.domain.entities.motokonig import MotoKonig
from app.domain.ports.repositories.motokonig import IMotoKonigRepository
from app.domain.ports.repositories.user import IUserRepository
from app.infrastructure.specs.motokonig.motokonig_by_user_id import MotoKonigByUserId

__all__ = ["CreateMotoKonigProfileUseCase"]


class CreateMotoKonigProfileUseCase:
    """Use case для создания профиля MotoKonig"""

    def __init__(
            self,
            motokonig_repo: IMotoKonigRepository,
            user_repo: IUserRepository,
    ):
        self._motokonig_repo = motokonig_repo
        self._user_repo = user_repo

    async def execute(
            self,
            user_id: UUID,
            nickname: str,
            bio: str | None = None,
            avatar_url: str | None = None,
            is_public: bool = True,
    ) -> MotoKonig:
        """Создать профиль MotoKonig для пользователя"""

        # Проверяем, существует ли пользователь
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Проверяем, нет ли уже профиля у пользователя
        existing = await self._motokonig_repo.get(MotoKonigByUserId(user_id))
        if existing:
            raise ValueError("MotoKonig profile already exists for this user")

        # Создаём профиль
        motokonig = MotoKonig(
            user_id=user_id,
            nickname=nickname,
            bio=bio,
            avatar_url=avatar_url,
            is_public=is_public,
        )

        # Сохраняем
        return await self._motokonig_repo.add(motokonig)
