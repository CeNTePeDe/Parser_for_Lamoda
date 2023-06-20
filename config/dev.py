import os

from pydantic import BaseSettings, HttpUrl


class Settings(BaseSettings):
    PROJECT_NAME: str = "Parser_Application"

    DEBUG: bool = os.environ.get("DEBUG")

    # MongoDB config
    MONGODB_HOST: str = os.environ.get("MONGODB_HOST")
    MONGODB_PORT: int = os.environ.get("MONGODB_PORT")
    MONGODB_USER: str = os.environ.get("MONGODB_USER")
    MONGODB_PASSWORD: str = os.environ.get("MONGODB_PASSWORD")
    MONGO_URL: HttpUrl = os.environ.get("MONGODB_URL")
    MONGODB_DB: str = os.environ.get("MONGODB_DB")

    # MongodDB Collections
    PRODUCT_COLLECTION = "products"

    USER_AGENT: int = os.environ.get("USER_AGENT")
    HEADERS: dict = {"User-Agent": os.environ.get("USER_AGENT")}

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
