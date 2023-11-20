from typing import List

from pydantic import MongoDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MongoDB
    MONGODB_URI: MongoDsn = "mongodb://db:27017/"  # type: ignore[assignment]
    MONGODB_DB_NAME: str = "certms"
    DEBUG: bool = True

    CORS_ORIGINS: List[str] = []

    UVICORN_HOST: str
    UVICORN_PORT: int

    class Config:
        env_file = ".env"
        case_sensitive = True


# Missing named arguments are filled with environment variables
settings = Settings()  # type: ignore[call-arg]
