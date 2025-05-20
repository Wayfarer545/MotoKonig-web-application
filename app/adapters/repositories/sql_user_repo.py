# app/adapters/repositories/sql_user_repo.py

from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.domain.ports.user_repository import IUserRepository, UserSpecificationPort
from app.domain.entities.user import User
from app.infrastructure.models.user_model import User as UserModel


class SqlUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User) -> User:
        db_user = UserModel(
            username=user.username,
            password_hash=user.password_hash,
            role=user.role,
            is_active=True
        )
        self.session.add(db_user)
        await self.session.flush()
        await self.session.refresh(db_user)
        user.id = db_user.id
        return user

    async def get(self, spec: UserSpecificationPort) -> Optional[User]:
        statement = spec.to_query(select(UserModel))
        result = await self.session.execute(statement)
        db_user = result.scalar_one_or_none()
        if db_user:
            return User(
                user_id=db_user.id,
                username=db_user.username,
                password_hash=db_user.password_hash,
                role=db_user.role
            )
        return None

    async def get_list(self) -> List[User]:
        result = await self.session.execute(select(UserModel))
        users = result.scalars().all()
        return [
            User(
                user_id=u.id,
                username=u.username,
                password_hash=u.password_hash,
                role=u.role
            )
            for u in users
        ]

    async def update(self, user: User) -> User:
        db_user = await self.session.get(UserModel, user.id)
        if db_user:
            db_user.username = user.username
            db_user.password_hash = user.password_hash
            db_user.role = user.role
            await self.session.flush()
        return user

    async def delete(self, user_id: UUID) -> bool:
        db_user = await self.session.get(UserModel, user_id)
        if db_user:
            await self.session.delete(db_user)
            await self.session.flush()
            return True
        return False
