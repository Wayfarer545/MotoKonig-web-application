# app/infrastructure/specs/ride/ride_with_available_slots.py

from typing import Any

from app.domain.ports.specs.ride import RideSpecificationPort
from app.infrastructure.models.ride import Ride as RideModel
from app.infrastructure.models.ride_participant import (
    RideParticipant as ParticipantModel,
)


class RideWithAvailableSlotsSpec(RideSpecificationPort):
    """Спецификация для поездок со свободными местами"""

    def to_query(self, base_query: Any) -> Any:
        from sqlalchemy import and_, func, select

        # Подзапрос для подсчёта активных участников
        participant_count_subquery = (
            select(func.count(ParticipantModel.id))
            .where(
                and_(
                    ParticipantModel.ride_id == RideModel.id,
                    ParticipantModel.left_at.is_(None)
                )
            )
            .scalar_subquery()
        )

        return base_query.where(
            participant_count_subquery < RideModel.max_participants,
            RideModel.is_completed == False # noqa: E712
        )
