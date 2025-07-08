from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_PREFIX: str

    BIND_HOST: str
    BIND_PORT: int = Field(8080, env="BIND_PORT")
    TELEGRAM_BOT_TOKEN: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    TELEGRAM_SECRET_TOKEN: str = Field(..., env="TELEGRAM_SECRET_TOKEN")
    WEBHOOK_URL: str = Field(..., env="WEBHOOK_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings(
    PROJECT_NAME="Telegram Bot API",
    API_PREFIX="/api/v1",
    BIND_HOST="0.0.0.0",
)
