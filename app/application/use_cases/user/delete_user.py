# app/application/use_cases/user/delete_user.py

from uuid import UUID

from domain.ports.repositories.user_repository import IUserRepository


class DeleteUserUseCase:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, user_id: UUID) -> bool:
        return await self.repo.delete(user_id)
