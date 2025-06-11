# app/infrastructure/repositories/sql_ride_repo.py

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.ride import Ride, RideCheckpoint, RideParticipant
from app.domain.ports.repositories.ride import IRideRepository
from app.domain.ports.specs.ride import RideSpecificationPort
from app.infrastructure.models.ride import Ride as RideModel
from app.infrastructure.models.ride_participant import (
    RideParticipant as ParticipantModel,
)

__all__ = ["SqlRideRepository"]


class SqlRideRepository(IRideRepository):
    """SQL реализация репозитория поездок"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain_entity(self, db_model: RideModel) -> Ride:
        """Преобразовать модель БД в доменную сущность"""
        participants = [
            RideParticipant(
                motokonig_id=UUID(p.motokonig_id),
                joined_at=p.joined_at,
                left_at=p.left_at,
                distance_covered=p.distance_covered,
                average_speed=p.average_speed,
                max_speed=p.max_speed,
                is_leader=p.is_leader,
            )
            for p in db_model.participants
        ]

        checkpoints = [
            RideCheckpoint(
                latitude=c.latitude,
                longitude=c.longitude,
                name=c.name,
                reached_at=c.reached_at,
            )
            for c in sorted(db_model.checkpoints, key=lambda x: x.order_index)
        ]

        return Ride(
            ride_id=UUID(db_model.id),
            organizer_id=UUID(db_model.organizer_id),
            title=db_model.title,
            description=db_model.description,
            difficulty=db_model.difficulty,
            planned_distance=db_model.planned_distance,
            max_participants=db_model.max_participants,
            start_location=db_model.start_location,
            end_location=db_model.end_location,
            planned_start=db_model.planned_start,
            planned_duration=db_model.planned_duration,
            actual_start=db_model.actual_start,
            actual_end=db_model.actual_end,
            actual_distance=db_model.actual_distance,
            route_gpx=db_model.route_gpx,
            weather_conditions=db_model.weather_conditions,
            participants=participants,
            checkpoints=checkpoints,
            is_public=db_model.is_public,
            is_completed=db_model.is_completed,
            rating=db_model.rating,
            created_at=db_model.created_at,
            updated_at=db_model.updated_at,
        )

    async def add(self, ride: Ride) -> Ride:
        """Создать новую поездку"""
        db_model = RideModel(
            organizer_id=str(ride.organizer_id),
            title=ride.title,
            description=ride.description,
            difficulty=ride.difficulty,
            planned_distance=ride.planned_distance,
            max_participants=ride.max_participants,
            start_location=ride.start_location,
            end_location=ride.end_location,
            planned_start=ride.planned_start,
            planned_duration=ride.planned_duration,
            route_gpx=ride.route_gpx,
            is_public=ride.is_public,
        )

        self.session.add(db_model)
        await self.session.flush()

        # Добавляем участников
        for participant in ride.participants:
            db_participant = ParticipantModel(
                ride_id=db_model.id,
                motokonig_id=str(participant.motokonig_id),
                joined_at=participant.joined_at,
                is_leader=participant.is_leader,
            )
            self.session.add(db_participant)

        await self.session.flush()
        await self.session.refresh(db_model)

        return self._to_domain_entity(db_model)

    async def get(self, spec: RideSpecificationPort) -> Ride | None:
        """Получить поездку по спецификации"""
        statement = spec.to_query(select(RideModel))
        result = await self.session.execute(statement)
        db_model = result.scalar_one_or_none()

        if db_model:
            return self._to_domain_entity(db_model)
        return None

    async def get_by_id(self, ride_id: UUID) -> Ride | None:
        """Получить поездку по ID"""
        from app.infrastructure.specs.ride.ride_by_id import RideById
        return await self.get(RideById(ride_id))

    async def get_list(self, spec: RideSpecificationPort | None = None) -> list[Ride]:
        """Получить список поездок"""
        statement = select(RideModel)

        if spec:
            statement = spec.to_query(statement)

        result = await self.session.execute(statement)
        db_models = result.scalars().all()

        return [self._to_domain_entity(model) for model in db_models]

    async def update(self, ride: Ride) -> Ride:
        """Обновить поездку"""
        db_model = await self.session.get(RideModel, str(ride.ride_id))

        if db_model:
            # Обновляем основные поля
            db_model.title = ride.title
            db_model.description = ride.description
            db_model.actual_start = ride.actual_start
            db_model.actual_end = ride.actual_end
            db_model.actual_distance = ride.actual_distance
            db_model.weather_conditions = ride.weather_conditions
            db_model.is_completed = ride.is_completed
            db_model.rating = ride.rating

            # TODO: Обновление участников (добавление/удаление)

            await self.session.flush()
            await self.session.refresh(db_model)

        return self._to_domain_entity(db_model)

    async def delete(self, ride_id: UUID) -> None:
        """Удалить поездку"""
        db_model = await self.session.get(RideModel, str(ride_id))
        if db_model:
            await self.session.delete(db_model)
            await self.session.flush()

    async def get_upcoming_rides(self, limit: int = 10) -> list[Ride]:
        """Получить предстоящие поездки"""
        from app.infrastructure.specs.ride.ride_upcoming import RideUpcomingSpec
        return await self.get_list(RideUpcomingSpec())

    async def get_rides_by_organizer(self, organizer_id: UUID) -> list[Ride]:
        """Получить поездки организатора"""
        from app.infrastructure.specs.ride.ride_by_organizer import RideByOrganizerSpec
        return await self.get_list(RideByOrganizerSpec(organizer_id))

    async def get_rides_by_participant(self, motokonig_id: UUID) -> list[Ride]:
        """Получить поездки участника"""
        # TODO: Реализовать спецификацию для поиска по участнику
        return []
