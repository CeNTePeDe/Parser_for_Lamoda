import json
import logging

from core.constant_variables import URL_STREAMERS, URL_STREAMERS_PARSE
from database import StreamerDAO

logger = logging.getLogger(__name__)

dao_streamer = StreamerDAO()


def test_get_streamers(client):
    response = client.get(url=URL_STREAMERS)

    assert response.status_code == 200
    assert len(response.json()) == len(dao_streamer.get_all_items())


def test_parse_streamer(client):
    response = client.post(url=URL_STREAMERS_PARSE)

    assert response.status_code == 200


def test_create_streamer(db, client, streamer):
    response = client.post(url=URL_STREAMERS, json=streamer)

    assert response.json() == 1
    assert response.status_code == 201


def test_get_streamer(db, client, streamer):
    id = "id_0"
    logger.info(f"id streamer {id} ")
    response = client.get(url=URL_STREAMERS + f"{id}")

    assert response.status_code == 200
    assert response.json()["id"] == "id_0"
    assert response.json()["user_id"] == "user_id_0"
    assert response.json()["title"] == "title_0"


def test_get_invalid_streamer(db, client):
    id = "invalid_id"
    response = client.get(url=URL_STREAMERS + f"{id}")

    assert response.status_code == 404


def test_update_streamer(db, streamer, streamer_build, client):
    new_streamer = streamer_build()
    id = "id_0"
    response = client.patch(url=URL_STREAMERS + f"{id}", json=new_streamer.dict())

    assert response.status_code == 200


def test_delete_streamer(db, client, streamer):
    id = streamer["id"]
    response = client.delete(url=URL_STREAMERS + f"{id}")

    assert response.status_code == 405
