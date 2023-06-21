import os
from types import ModuleType

import config
from config.dev import SettingsDev
from config.prod import SettingsProd
from config.stage import SettingsStage


def set_environment(environment: str) -> ModuleType:
    if environment == "dev":
        return config.dev
    if environment == "prod":
        return config.prod
    if environment == "stage":
        return config.stage
    else:
        raise ValueError("Invalid environment")


env = os.environ.setdefault("ENV", "dev")
environment = set_environment(env)

