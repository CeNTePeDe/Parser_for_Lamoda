import logging
from typing import Optional

import requests
from pydantic import AnyUrl

from core.constant_variables import BASE_URL, HEADERS_TWITCH
from core.exception import InvalidUrlInputError

logger = logging.getLogger(__name__)


def get_data_stream(url: AnyUrl, offset: Optional[int] = None) -> list[dict]:
    logger.info("get_data_stream is started")
    params = {"first": offset}
    if url != BASE_URL:
        raise InvalidUrlInputError(name=url)
    response = requests.get(url, headers=HEADERS_TWITCH, params=params)
    data_streamers = response.json()["data"]
    logger.info("get_data_stream is finished successfully")
    logger.info(f"list_streamers is {data_streamers}")
    return data_streamers
