from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    API_PREFIX: str

    BIND_HOST: str
    BIND_PORT: int


settings = Settings(
    PROJECT_NAME="Telegram Bot API",
    API_PREFIX="/api/v1",
    BIND_HOST="0.0.0.0",
    BIND_PORT=8080,
)