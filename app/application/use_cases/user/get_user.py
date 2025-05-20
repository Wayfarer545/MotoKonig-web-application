# app/application/use_cases/user/get_user.py

from typing import Optional
from uuid import UUID
from app.domain.entities.user import User
from app.domain.ports.user_repository import IUserRepository
from app.domain.specifications.user_by_id import UserById  # переносим из user_specs

class GetUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, user_id: UUID) -> Optional[User]:
        spec = UserById(user_id)
        return await self.repo.get(spec)
