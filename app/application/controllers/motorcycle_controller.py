# app/application/controllers/motorcycle_controller.py

from uuid import UUID

from app.application.exceptions import NotFoundError
from app.application.use_cases.motorcycle.create_motorcycle import (
    CreateMotorcycleUseCase,
)
from app.application.use_cases.motorcycle.delete_motorcycle import (
    DeleteMotorcycleUseCase,
)
from app.application.use_cases.motorcycle.get_motorcycle import GetMotorcycleUseCase
from app.application.use_cases.motorcycle.list_motorcycles import ListMotorcyclesUseCase
from app.application.use_cases.motorcycle.update_motorcycle import (
    UpdateMotorcycleUseCase,
)
from app.domain.entities.motorcycle import Motorcycle
from app.domain.value_objects.engine_type import EngineType
from app.domain.value_objects.motorcycle_type import MotorcycleType
from app.infrastructure.specs.moto.moto_by_id import (
    MotorcycleById,
)
from app.infrastructure.specs.moto.moto_by_owner import (
    MotorcyclesByOwner,
)
from app.infrastructure.specs.moto.moto_search import (
    MotorcycleSearch,
)


class MotorcycleController:
    """Контроллер для управления мотоциклами"""

    def __init__(
            self,
            list_uc: ListMotorcyclesUseCase,
            get_uc: GetMotorcycleUseCase,
            create_uc: CreateMotorcycleUseCase,
            update_uc: UpdateMotorcycleUseCase,
            delete_uc: DeleteMotorcycleUseCase,
    ):
        self.list_uc = list_uc
        self.get_uc = get_uc
        self.create_uc = create_uc
        self.update_uc = update_uc
        self.delete_uc = delete_uc

    async def create_motorcycle(
            self,
            owner_id: UUID,
            brand: str,
            model: str,
            year: int,
            engine_volume: int,
            engine_type: EngineType,
            motorcycle_type: MotorcycleType,
            power: int | None = None,
            mileage: int | None = None,
            color: str | None = None,
            description: str | None = None,
    ) -> Motorcycle:
        """Создать новый мотоцикл"""
        return await self.create_uc.execute(
            owner_id=owner_id,
            brand=brand,
            model=model,
            year=year,
            engine_volume=engine_volume,
            engine_type=engine_type,
            motorcycle_type=motorcycle_type,
            power=power,
            mileage=mileage,
            color=color,
            description=description,
        )

    async def get_motorcycle_by_id(self, motorcycle_id: UUID) -> dict:
        """Получить мотоцикл по ID"""
        spec = MotorcycleById(motorcycle_id)
        motorcycle = await self.get_uc.execute(spec)

        if not motorcycle:
            raise NotFoundError("Motorcycle not found")

        return motorcycle.to_dto()

    async def get_user_motorcycles(
            self,
            owner_id: UUID,
            active_only: bool = True
    ) -> list[dict]:
        """Получить мотоциклы пользователя"""
        spec = MotorcyclesByOwner(owner_id, active_only)
        motorcycles = await self.list_uc.execute(spec)
        return [m.to_dto() for m in motorcycles]

    async def search_motorcycles(
            self,
            brand: str | None = None,
            model: str | None = None,
            year_from: int | None = None,
            year_to: int | None = None,
            motorcycle_type: MotorcycleType | None = None,
            engine_type: EngineType | None = None,
            engine_volume_from: int | None = None,
            engine_volume_to: int | None = None,
            power_from: int | None = None,
            power_to: int | None = None,
            active_only: bool = True
    ) -> list[dict]:
        """Поиск мотоциклов с фильтрами"""
        spec = MotorcycleSearch(
            brand=brand,
            model=model,
            year_from=year_from,
            year_to=year_to,
            motorcycle_type=motorcycle_type,
            engine_type=engine_type,
            engine_volume_from=engine_volume_from,
            engine_volume_to=engine_volume_to,
            power_from=power_from,
            power_to=power_to,
            active_only=active_only
        )
        motorcycles = await self.list_uc.execute(spec)
        return [m.to_dto() for m in motorcycles]

    async def update_motorcycle(
            self,
            motorcycle_id: UUID,
            brand: str | None = None,
            model: str | None = None,
            year: int | None = None,
            engine_volume: int | None = None,
            engine_type: EngineType | None = None,
            motorcycle_type: MotorcycleType | None = None,
            power: int | None = None,
            mileage: int | None = None,
            color: str | None = None,
            description: str | None = None,
            is_active: bool | None = None,
    ) -> dict:
        """Обновить мотоцикл"""
        updated = await self.update_uc.execute(
            motorcycle_id=motorcycle_id,
            brand=brand,
            model=model,
            year=year,
            engine_volume=engine_volume,
            engine_type=engine_type,
            motorcycle_type=motorcycle_type,
            power=power,
            mileage=mileage,
            color=color,
            description=description,
            is_active=is_active,
        )

        if not updated:
            raise NotFoundError("Motorcycle not found")

        return updated.to_dto()

    async def delete_motorcycle(self, motorcycle_id: UUID) -> None:
        """Удалить мотоцикл"""
        success = await self.delete_uc.execute(motorcycle_id)
        if not success:
            raise NotFoundError("Motorcycle not found")
