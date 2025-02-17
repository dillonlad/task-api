from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # Basic app env vars
    APP_NAME: str = "Task API"
    VERSION: str = "0.0.0"
    DEBUG: bool = False

    # CORS env vars
    ALLOWED_METHODS: list[str] = ["*"]
    ALLOWED_HEADERS: list[str] = ["*"]
    ORIGINS: list[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True


def get_config():
    return Config()
