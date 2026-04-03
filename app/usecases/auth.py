from app.repositories.users import UserRepository
from app.core.security import hash_pwd, verify_pwd, create_access_token
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError

class AuthUseCase:
    """Бизнес-логика регистрации, логина и получения профиля."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register(self, email: str, password: str) -> dict:
        """
        Регистрация нового пользователя.
        Возвращает публичные данные пользователя (id, email, role).
        """
        # Проверяем, не занят ли email
        existing = await self.user_repo.get_by_email(email)
        if existing:
            raise ConflictError("User with this email already exists")

        # Хешируем пароль
        hashed = hash_pwd(password)

        # Создаём пользователя через репозиторий
        user = await self.user_repo.create(email, hashed)

        # Возвращаем публичные данные (без пароля)
        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }

    async def login(self, email: str, password: str) -> dict:
        """
        Аутентификация пользователя.
        Возвращает access_token и его тип.
        """
        # Ищем пользователя по email
        user = await self.user_repo.get_by_email(email)
        if not user:
            raise UnauthorizedError("Incorrect email or password")

        # Проверяем пароль
        if not verify_pwd(password, user.hash_pwd):
            raise UnauthorizedError("Incorrect email or password")

        # Генерируем JWT access token
        access_token = create_access_token(
            sub=str(user.id),
            role=user.role
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    async def get_profile(self, user_id: int) -> dict:
        """
        Получение публичного профиля пользователя по id.
        """
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
        }