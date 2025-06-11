# app/application/use_cases/event/delete_event.py
from uuid import UUID

from app.domain.ports.repositories.event import IEventRepository


class DeleteEventUseCase:
    """Use case для удаления мероприятия"""

    def __init__(self, repo: IEventRepository):
        self.repo = repo

    async def execute(self, event_id: UUID) -> bool:
        return await self.repo.delete(event_id)
