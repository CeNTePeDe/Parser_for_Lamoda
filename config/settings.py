import os
from typing import Optional, Union

from pymongo import MongoClient

from config import SettingsDev, SettingsProd, SettingsStage

env = os.environ.setdefault("APPLICATION_CONFIG", "dev")


def init_settings(
    environment: Optional[str] = None,
) -> Union[SettingsDev, SettingsProd, SettingsStage]:
    if environment == "prod":
        return SettingsProd()
    elif environment == "stage":
        return SettingsStage()
    return SettingsDev()


settings = init_settings(env)


def get_db(db_name=settings.MONGODB_DB):
    client = MongoClient(settings.MONGO_URL)
    db = client.get_database(db_name)
    return db
