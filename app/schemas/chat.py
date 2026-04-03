from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    """
    Схема запроса к чату.
    """
    prompt: str = Field(..., description="Основной текст запроса пользователя")
    system: Optional[str] = Field(None, description="Необязательная системная инструкция для модели")
    max_history: Optional[int] = Field(10, description="Количество последних сообщений из истории, которые будут учтены", ge=1)
    temperature: Optional[float] = Field(0.7, description="Креативность модели (0 — детерминированно, 1 — высокая случайность)", ge=0.0, le=2.0)

class ChatResponse(BaseModel):
    """
    Схема ответа чата.
    """
    answer: str = Field(..., description="Ответ языковой модели")

class ChatMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime