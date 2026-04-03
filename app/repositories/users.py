from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import User

class UserRepository:
    """Репозиторий для работы с пользователями (только операции доступа к данным)."""

    def __init__(self, session: AsyncSession):
        self._session = session  # приватное поле

    async def get_by_email(self, email: str) -> User | None:
        """Получить пользователя по email."""
        stmt = select(User).where(User.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        """Получить пользователя по id."""
        stmt = select(User).where(User.id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, email: str, hash_pwd: str) -> User:
        """
        Создать нового пользователя.
        Пароль должен быть уже захэширован (вызов этого метода не занимается хешированием).
        """
        user = User(
            email=email,
            hash_pwd=hash_pwd,
            role="user",
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user