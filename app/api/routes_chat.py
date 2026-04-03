from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.chat import ChatRequest, ChatResponse, ChatMessageResponse
from app.usecases.chat import ChatUseCase
from app.api.deps import get_chat_usecase, get_current_user_id
from app.core.errors import ExternalServiceError

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    chat_uc: ChatUseCase = Depends(get_chat_usecase),
):
    """Отправить сообщение и получить ответ LLM."""
    try:
        answer = await chat_uc.ask(
            user_id=user_id,
            prompt=request.prompt,
            system=request.system,
            temperature=request.temperature,
            max_history=request.max_history,
        )
    except ExternalServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"LLM service error: {e.detail}",
        )
    return ChatResponse(answer=answer)

@router.get("/chat/history", response_model=list[ChatMessageResponse])
async def get_history(
    user_id: int = Depends(get_current_user_id),
    chat_uc: ChatUseCase = Depends(get_chat_usecase),
):
    """Получить историю сообщений пользователя."""
    messages = await chat_uc.get_history(user_id)
    return [
        ChatMessageResponse(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at,
        )
        for msg in messages
    ]

@router.delete("/chat/history", status_code=status.HTTP_204_NO_CONTENT)
async def clear_history(
    user_id: int = Depends(get_current_user_id),
    chat_uc: ChatUseCase = Depends(get_chat_usecase),
):
    """Очистить всю историю сообщений пользователя."""
    await chat_uc.clear_history(user_id)
    return None