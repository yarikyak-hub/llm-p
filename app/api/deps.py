from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.auth import AuthUseCase
from app.usecases.chat import ChatUseCase
from app.core.security import decode_token

# OAuth2 схема для Swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ----------------------------------------------------------------------
# БД и репозитории
# ----------------------------------------------------------------------
async def get_db() -> AsyncSession:
    """Предоставляет асинхронную сессию базы данных."""
    async with AsyncSessionLocal() as session:
        yield session

def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    """Фабрика репозитория пользователей."""
    return UserRepository(db)

def get_chat_message_repo(db: AsyncSession = Depends(get_db)) -> ChatMessageRepository:
    """Фабрика репозитория сообщений чата."""
    return ChatMessageRepository(db)

# ----------------------------------------------------------------------
# Клиенты внешних сервисов
# ----------------------------------------------------------------------
def get_openrouter_client() -> OpenRouterClient:
    """Фабрика клиента OpenRouter (синглтон)."""
    return OpenRouterClient()

# ----------------------------------------------------------------------
# Usecases
# ----------------------------------------------------------------------
def get_auth_usecase(user_repo: UserRepository = Depends(get_user_repo)) -> AuthUseCase:
    """Фабрика usecase аутентификации."""
    return AuthUseCase(user_repo)

def get_chat_usecase(
    message_repo: ChatMessageRepository = Depends(get_chat_message_repo),
    client: OpenRouterClient = Depends(get_openrouter_client),
) -> ChatUseCase:
    """Фабрика usecase чата."""
    return ChatUseCase(message_repo, client)

# ----------------------------------------------------------------------
# Зависимости для получения текущего пользователя
# ----------------------------------------------------------------------
async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """
    Извлекает user_id из JWT access token. При ошибках аутентификации выбрасывает HTTP 401.
    """
    try:
        payload = decode_token(token)          # доменная функция, выбрасывает ValueError
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token payload does not contain 'sub'",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return int(user_id)
    except ValueError as e:
        # Ошибки: просроченный токен, неверная подпись, некорректный формат
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )