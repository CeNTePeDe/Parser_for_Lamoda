import logging.config
import os
from typing import Union, Optional

from fastapi import FastAPI
from config import SettingsDev, SettingsProd, SettingsStage

from routers.product import routers


def init_settings(environment: Optional[str] = None) -> Union[SettingsDev, SettingsProd, SettingsStage]:
    if environment == "prod":
        return SettingsProd()
    elif environment == "stage":
        return SettingsStage()
    return SettingsDev()


env = os.environ.setdefault("APPLICATION_CONFIG", "dev")
settings = init_settings(env)

logging.config.dictConfig(settings.LOGGING_CONFIG)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(routers, tags=["Products"], prefix="/api/products")

