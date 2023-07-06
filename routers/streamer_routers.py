import logging
from typing import Optional

from fastapi import APIRouter, status

from database import StreamerDAO
from models.streamers_models import StreamerIn, StreamerOut
from parsers.parse_streamer import get_data_stream

logger = logging.getLogger(__name__)

streamer_routers = APIRouter()
streamer_dao = StreamerDAO()


@streamer_routers.get("/", status_code=status.HTTP_200_OK)
async def get_streamers() -> list[StreamerOut]:
    return streamer_dao.sort_item()


@streamer_routers.post("/parsing_streamers/", status_code=status.HTTP_200_OK)
async def get_streamers_from_twitch(offset: Optional[int] = None) -> list[StreamerOut]:
    list_streamers = get_data_stream(offset=offset)
    for streamer in list_streamers:
        streamer_dao.create_item(StreamerIn(**streamer))
        logger.info(f"streamer is {streamer}")
    return streamer_dao.get_all_item()


@streamer_routers.get("/{id}", status_code=status.HTTP_200_OK)
async def get_streamer(id: str) -> StreamerIn:
    return streamer_dao.get_item(id=id)


@streamer_routers.post("/", status_code=status.HTTP_201_CREATED)
async def create_streamer(streamer: StreamerIn) -> int:
    return streamer_dao.create_item(streamer_data=streamer)


@streamer_routers.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_streamer(id: str, streamer_data: StreamerIn) -> int:
    return streamer_dao.update_item(id=id, streamer_data=streamer_data)


@streamer_routers.delete("/{id} ", status_code=status.HTTP_204_NO_CONTENT)
async def delete_streamer(id: str) -> None:
    streamer_dao.delete_item(id=id)
