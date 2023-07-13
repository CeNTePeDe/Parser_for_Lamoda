import os

from pydantic import BaseSettings


class SettingsDev(BaseSettings):
    PROJECT_NAME: str = "Parser_Application"

    DEBUG: bool = os.environ.get("DEBUG")

    # MongoDB config
    MONGODB_HOST: str = os.environ.get("MONGODB_HOST")
    MONGODB_PORT: int = os.environ.get("MONGODB_PORT")
    MONGODB_USER: str = os.environ.get("MONGODB_USER")
    MONGODB_PASSWORD: str = os.environ.get("MONGODB_PASSWORD")
    MONGO_URL: str = os.environ.get("MONGO_URL")
    MONGODB_DB: str = os.environ.get("MONGODB_DB")

    # Mongo_DB Collections
    PRODUCT_COLLECTION = "products"
    # Kafka
    KAFKA_URL: str = os.environ.get("KAFKA_URL")
    TOPIC_PRODUCT: str = "product_parser"
    TOPIC_STREAMER: str = "streamer_parser"
    CONSUMER_TIMEOUT_MS: int = 1000
    AUTO_OFFSET_RESET: str = "earliest"

    HEADERS_TWITCH: dict = {
        "Client-ID": os.environ.get("ID"),
        "Authorization": os.environ.get("TOKEN"),
    }

    LOGGING_CONFIG: dict = {
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

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"
