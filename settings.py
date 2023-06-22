from typing import Union

from config.dev import SettingsDev
from config.prod import SettingsProd
from config.stage import SettingsStage


def init_settings(environment: str) -> Union[SettingsDev, SettingsProd, SettingsStage]:
    if environment == "prod":
        return SettingsProd()
    elif environment == "stage":
        return SettingsStage()
    return SettingsDev()

