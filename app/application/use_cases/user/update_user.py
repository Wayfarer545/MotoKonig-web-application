# app/application/use_cases/user/update_user.py
from uuid import UUID
from typing import Optional
from app.domain.entities.user import User, UserRole
from app.domain.ports.user_repository import IUserRepository
from app.domain.ports.password_service import PasswordService
from app.domain.specifications.user_by_id import UserById

class UpdateUserUseCase:
    def __init__(self, repo: IUserRepository, pwd_service: PasswordService):
        self.repo = repo
        self.pwd_service = pwd_service

    async def execute(
        self,
        user_id: UUID,
        new_username: Optional[str] = None,
        new_password: Optional[str] = None,
        new_role: Optional[UserRole] = None,
        deactivate: bool = False,
    ) -> Optional[User]:
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
