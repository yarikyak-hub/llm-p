import httpx
from app.core.config import settings
from app.core.errors import ExternalServiceError

class OpenRouterClient:
    """Клиент для взаимодействия с API OpenRouter."""

    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY.get_secret_value()
        self.base_url = settings.OPENROUTER_BASE_URL
        self.model = settings.OPENROUTER_MODEL
        self.site_url = settings.OPENROUTER_SITE_URL
        self.app_name = settings.OPENROUTER_APP_NAME

    async def chat_completion(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str:
        """
        Отправляет запрос к OpenRouter и возвращает текст ответа модели.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.app_name,
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                # Извлекаем текст ответа (стандартный формат OpenAI)
                return data["choices"][0]["message"]["content"]
            except httpx.HTTPStatusError as e:
                raise ExternalServiceError(
                    f"OpenRouter returned error {e.response.status_code}: {e.response.text}"
                )
            except httpx.RequestError as e:
                raise ExternalServiceError(f"OpenRouter request failed: {str(e)}")
            except (KeyError, IndexError) as e:
                raise ExternalServiceError(f"Unexpected OpenRouter response format: {str(e)}")