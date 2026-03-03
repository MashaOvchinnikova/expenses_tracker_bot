from pathlib import Path
from typing import Optional, Any

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
       Настройки приложения.

       Все значения автоматически загружаются из .env файла
       или из переменных окружения системы.
    """
    # Telegram
    BOT_TOKEN: SecretStr

    # Database - либо готовая строка, либо компоненты
    DATABASE_URL: Optional[str] = None
    POSTGRES_USER: str
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # App
    DEBUG: bool
    API_V1_PREFIX: str

    # JWT Settings
    SECRET_KEY: str = SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


    model_config = SettingsConfigDict(
        env_file = str(Path(__file__).parent.parent.parent / ".env"),  # загружаем из .env
        env_file_encoding="utf-8",
        case_sensitive=False,  # имена переменных не чувствительны к регистру
        extra="ignore"  # игнорировать лишние переменные
    )

    def __init__(self, **values: Any):
        super().__init__(**values)
        # Если DATABASE_URL не указан, собираем из компонентов
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD.get_secret_value()}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )

def get_settings() -> BaseSettings:
    """Возвращает объект настроек"""
    return Settings()

# Глобальный объект настроек
settings = get_settings()