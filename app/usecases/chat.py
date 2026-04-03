from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient
from app.core.errors import ExternalServiceError

class ChatUseCase:
    """Бизнес-логика общения с LLM через OpenRouter."""

    def __init__(
        self,
        message_repo: ChatMessageRepository,
        openrouter_client: OpenRouterClient,
    ):
        self.message_repo = message_repo
        self.openrouter_client = openrouter_client

    async def ask(
        self,
        user_id: int,
        prompt: str,
        system: str | None = None,
        max_history: int = 10,
        temperature: float = 0.7,
    ) -> str:
        """
        Обрабатывает запрос пользователя:
        - сохраняет prompt в БД,
        - формирует контекст из истории,
        - вызывает OpenRouter,
        - сохраняет ответ ассистента,
        - возвращает ответ.
        """
        # 1. Сохраняем сообщение пользователя
        await self.message_repo.add_message(
            user_id=user_id,
            role="user",
            content=prompt,
        )

        # 2. Загружаем историю пользователя
        history = await self.message_repo.get_last_messages(user_id, limit=max_history)

        # 3. Формируем список messages для OpenRouter
        messages = []

        # Системная инструкция, при наличии
        if system:
            messages.append({"role": "system", "content": system})

        # История: сообщения уже в правильном порядке (старые → новые)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        # Текущий запрос (уже сохранён, но его ещё нет в истории, потому что добавили после получения истории)
        # Добавляем его в messages для запроса к LLM
        messages.append({"role": "user", "content": prompt})

        # 4. Вызываем OpenRouter
        try:
            assistant_answer = await self.openrouter_client.chat_completion(
                messages=messages,
                temperature=temperature,
            )
        except ExternalServiceError:
            # Пробрасываем дальше, чтобы роутер обработал
            raise

        # 5. Сохраняем ответ ассистента в БД
        await self.message_repo.add_message(
            user_id=user_id,
            role="assistant",
            content=assistant_answer,
        )

        return assistant_answer
    
    async def get_history(self, user_id: int, limit: int = 100) -> list[ChatMessageRepository]:
    # Вернуть историю сообщений пользователя (последние limit записей)
        return await self.message_repo.get_last_messages(user_id, limit)

    async def clear_history(self, user_id: int) -> None:
        # Удалить всю историю сообщений пользователя
        await self.message_repo.delete_user_history(user_id)