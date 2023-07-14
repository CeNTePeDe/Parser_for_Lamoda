import json
import logging
from typing import Optional

from fastapi import APIRouter, HTTPException, status

from database import StreamerDAO
from kafka_producers.kafka_streamers import (kafka_consumer_for_streamers,
                                             send_data_to_kafka_streamers)
from models.streamers_models import StreamerIn, StreamerOut
from parsers.parse_streamer import get_data_streams

logger = logging.getLogger(__name__)

streamer_routers = APIRouter()
streamer_dao = StreamerDAO()


@streamer_routers.get("/", status_code=status.HTTP_200_OK)
async def get_streamers() -> list[StreamerOut]:
    return streamer_dao.sort_item()


@streamer_routers.post("/parsing_streamers/", status_code=status.HTTP_200_OK)
async def get_streamers_from_twitch(offset: Optional[int] = None) -> list[StreamerOut]:
    list_streamers = get_data_streams(offset=offset)
    logger.info("send data to kafka")
    send_data_to_kafka_streamers(list_streamers)

    streamers = kafka_consumer_for_streamers()
    for streamer in streamers:
        streamer = json.loads(streamer.value)
        streamer_dao.create_item(StreamerIn(**streamer))
        logger.info(f"streamer is {streamer}")

    return streamer_dao.get_all_items()


@streamer_routers.get("/{id}", status_code=status.HTTP_200_OK)
async def get_streamer(id: str) -> StreamerIn:
    streamer = streamer_dao.get_item(id=id)
    if streamer is None:
        raise HTTPException(status_code=404, detail="Streamer not found")
    return streamer


@streamer_routers.post("/", status_code=status.HTTP_201_CREATED)
async def create_streamer(streamer: StreamerIn) -> int:
    return streamer_dao.create_item(streamer_data=streamer)


@streamer_routers.patch("/{id}", status_code=status.HTTP_200_OK)
async def update_streamer(id: str, streamer_data: StreamerIn) -> Optional[int]:
    streamer_updated = streamer_dao.update_item(id=id, streamer_data=streamer_data)
    if streamer_updated == 0:
        raise HTTPException(status_code=404, detail="Streamer not found")
    return streamer_updated


@streamer_routers.delete("/{id} ", status_code=status.HTTP_204_NO_CONTENT)
async def delete_streamer(id: str) -> None:
    deleted_streamers = streamer_dao.delete_item(id=id)
    if deleted_streamers == 0:
        raise HTTPException(status_code=404, detail="Streamer not found")
