import logging.config
import os
from typing import Optional, Union

from fastapi import FastAPI

from config import SettingsDev, SettingsProd, SettingsStage
from core.exception import InvalidUrlInputError
from core.exception_handler import exception_404_handler
from routers.product import routers


def init_settings(
    environment: Optional[str] = None,
) -> Union[SettingsDev, SettingsProd, SettingsStage]:
    if environment == "prod":
        return SettingsProd()
    elif environment == "stage":
        return SettingsStage()
    return SettingsDev()


env = os.environ.setdefault("APPLICATION_CONFIG", "dev")
settings = init_settings(env)

logging.config.dictConfig(settings.LOGGING_CONFIG)

app = FastAPI(title=settings.PROJECT_NAME)

app.add_exception_handler(InvalidUrlInputError, exception_404_handler)
app.include_router(routers, tags=["Products"], prefix="/api/products")
