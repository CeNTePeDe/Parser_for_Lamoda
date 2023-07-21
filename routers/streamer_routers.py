import json
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status

from database import StreamerDAO
from kafka_producers.kafka_streamers import (consumer_streamer,
                                             send_data_to_kafka_streamers)
from models.streamers_models import StreamerIn, StreamerOut
from parsers.parse_streamer import get_data_streams

logger = logging.getLogger(__name__)

streamer_routers = APIRouter()


@streamer_routers.get("/", status_code=status.HTTP_200_OK)
async def get_streamers(streamer_dao=Depends(StreamerDAO)) -> list[StreamerOut]:
    return streamer_dao.sort_item()


@streamer_routers.post("/parsing_streamers/", status_code=status.HTTP_200_OK)
async def get_streamers_from_twitch(
        offset: Optional[int] = None, streamer_dao=Depends(StreamerDAO)
) -> list[StreamerOut]:
    list_streamers = get_data_streams(offset=offset)
    logger.info("send data to kafka")
    send_data_to_kafka_streamers(list_streamers)

    for streamer in consumer_streamer:
        streamer = json.loads(streamer.value)
        streamer_dao.create_item(StreamerIn(**streamer))
        logger.info(f"streamer is {streamer}")

    return streamer_dao.get_all_items()


@streamer_routers.get("/{id}", status_code=status.HTTP_200_OK)
async def get_streamer(id: str, streamer_dao=Depends(StreamerDAO)) -> StreamerIn:
    streamer = streamer_dao.get_item(id=id)
    if streamer is None:
        raise HTTPException(status_code=404, detail="Streamer not found")
    return streamer


@streamer_routers.get("/game/{game_name}", status_code=status.HTTP_200_OK)
async def get_streamers_by_game(
        game_name: str, streamer_dao=Depends(StreamerDAO)
) -> list[StreamerOut]:
    list_streamers = streamer_dao.get_item_by_game(game_name=game_name)
    if len(list_streamers) == 0:
        raise HTTPException(
            status_code=404, detail=f"Streamers by {game_name} not found"
        )
    return list_streamers


@streamer_routers.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=StreamerIn
)
async def create_streamer(
        streamer: StreamerIn, streamer_dao=Depends(StreamerDAO)
) -> StreamerIn:
    return streamer_dao.create_item(streamer_data=streamer)


@streamer_routers.patch(
    "/{id}", status_code=status.HTTP_200_OK, response_model=StreamerIn
)
async def update_streamer(
        id: str, streamer_data: StreamerIn, streamer_dao=Depends(StreamerDAO)
) -> StreamerIn:
    streamer_updated = streamer_dao.update_item(id=id, streamer_data=streamer_data)
    if streamer_updated == 0:
        raise HTTPException(status_code=404, detail="Streamer not found")
    return streamer_updated


@streamer_routers.delete("/{id} ", status_code=status.HTTP_204_NO_CONTENT)
async def delete_streamer(id: str, streamer_dao=Depends(StreamerDAO)) -> None:
    deleted_streamers = streamer_dao.delete_item(id=id)
    if deleted_streamers == 0:
        raise HTTPException(status_code=404, detail="Streamer not found")
