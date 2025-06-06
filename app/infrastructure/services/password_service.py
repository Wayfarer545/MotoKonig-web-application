import bcrypt

from app.domain.ports.password_service import PasswordService


class PasswordServiceImpl(PasswordService):
    async def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    async def verify(self, password: str, pwd_hash: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), pwd_hash.encode("utf-8"))

