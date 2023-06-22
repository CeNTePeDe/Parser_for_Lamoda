import logging.config
import os

from fastapi import FastAPI

from settings import init_settings

env = os.environ.setdefault("APPLICATION_CONFIG", "dev")
settings = init_settings(env)

logging.config.dictConfig(settings.LOGGING_CONFIG)

app = FastAPI(title=settings.PROJECT_NAME)

