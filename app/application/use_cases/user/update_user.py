# app/application/use_cases/user/update_user.py

from uuid import UUID

from app.domain.entities.user import User, UserRole
from app.domain.ports.password_service import PasswordService
from app.domain.ports.user_repository import IUserRepository
from app.infrastructure.specs.user.user_by_id import UserById


class UpdateUserUseCase:
    def __init__(self, repo: IUserRepository, pwd_service: PasswordService):
        self.repo = repo
        self.pwd_service = pwd_service

    async def execute(
        self,
        user_id: UUID,
        new_username: str | None = None,
        new_password: str | None = None,
        new_role: UserRole | None = None,
        deactivate: bool = False,
    ) -> User | None:
        existing = await self.repo.get(UserById(user_id))
        if not existing:
            return None

        if new_username:
            existing.change_username(new_username)
        if new_password:
            existing.password_hash = await self.pwd_service.hash(new_password)
        if new_role:
            existing.role = new_role
        if deactivate:
            existing.deactivate()

        return await self.repo.update(existing)
