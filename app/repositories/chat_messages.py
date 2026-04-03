from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import ChatMessage

class ChatMessageRepository:
    """Репозиторий для работы с сообщениями чата (только операции доступа к данным)."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        """
        Добавить сообщение в историю чата.
        role: 'user' или 'assistant'
        """
        message = ChatMessage(
            user_id=user_id,
            role=role,
            content=content,
        )
        self._session.add(message)
        await self._session.commit()
        await self._session.refresh(message)
        return message

    async def get_last_messages(self, user_id: int, limit: int = 10) -> list[ChatMessage]:
        """
        Получить последние limit сообщений пользователя, отсортированные по времени создания (от старых к новым).
        """
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.asc())
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def delete_user_history(self, user_id: int) -> None:
        """Удалить все сообщения пользователя."""
        stmt = delete(ChatMessage).where(ChatMessage.user_id == user_id)
        await self._session.execute(stmt)
        await self._session.commit()