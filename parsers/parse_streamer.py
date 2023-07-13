import logging
from typing import Optional

import requests

from core.constant_variables import BASE_URL

logger = logging.getLogger(__name__)


def get_data_streams(offset: Optional[int] = None) -> list[dict]:
    from main import settings

    logger.info("get_data_stream is started")
    params = {"first": offset}
    response = requests.get(BASE_URL, headers=settings.HEADERS_TWITCH, params=params)
    data_streamers = response.json()["data"]
    logger.info("get_data_stream is finished successfully")
    logger.info(f"list_streamers is {data_streamers}")
    return data_streamers
