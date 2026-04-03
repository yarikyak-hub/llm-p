from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    ENV: str

    JWT_SECRET: str
    JWT_ALG: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    SQLITE_PATH: str

    OPENROUTER_API_KEY: SecretStr
    OPENROUTER_BASE_URL: str
    OPENROUTER_MODEL: str
    OPENROUTER_SITE_URL: str
    OPENROUTER_APP_NAME: str

    # Для подгрузки данных из .env
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=False,
        )

# Создание единственного экземпляра настроек
settings = Settings()