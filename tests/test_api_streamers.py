import logging

from core.constant_variables import URL_STREAMERS, URL_STREAMERS_PARSE
from tests.factories import StreamerInFactory

logger = logging.getLogger(__name__)


def test_get_streamers(client):
    response = client.get(url=URL_STREAMERS)

    assert response.status_code == 200


def test_parse_streamer(client, mongo_mock):
    response = client.post(url=URL_STREAMERS_PARSE)

    assert response.status_code == 200


def test_create_streamer(client, mongo_mock):
    data = StreamerInFactory.build()

    payload = {
        "id": data.id,
        "user_id": data.user_id,
        "user_login": data.user_login,
        "user_name": data.user_name,
        "game_id": data.game_id,
        "game_name": data.game_name,
        "type": data.type,
        "title": data.title,
        "viewer_count": data.viewer_count,
        "started_at": data.started_at,
        "language": data.language,
        "thumbnail_url": data.thumbnail_url,
        "tag_ids": data.tag_ids,
        "tags": data.tags,
        "is_mature": data.is_mature,
    }
    logger.info(f"Payload {payload}")
    response = client.post(url=URL_STREAMERS, json=payload)

    assert response.status_code == 201


def test_get_streamer(client, mongo_mock):
    id = "1111111"

    response = client.get(url=URL_STREAMERS + f"{id}")

    assert response.status_code == 200


def test_get_invalid_streamer_id(client, mongo_mock):
    id = "invalid_product"

    response = client.get(url=URL_STREAMERS + f"{id}")

    assert response.status_code == 404


def test_update_streamer(client, mongo_mock):
    id = "1111111"
    data = StreamerInFactory.build()

    payload = {
        "id": data.id,
        "user_id": data.user_id,
        "user_login": data.user_login,
        "user_name": data.user_name,
        "game_id": data.game_id,
        "game_name": data.game_name,
        "type": data.type,
        "title": data.title,
        "viewer_count": data.viewer_count,
        "started_at": data.started_at,
        "language": data.language,
        "thumbnail_url": data.thumbnail_url,
        "tag_ids": data.tag_ids,
        "tags": data.tags,
        "is_mature": data.is_mature,
    }
    logger.info(f"Payload {payload}")

    response = client.patch(url=URL_STREAMERS + f"{id}", json=payload)

    assert response.status_code == 200


def test_invalid_update_streamer(client, mongo_mock):
    id = "invalid_id"
    data = StreamerInFactory.build()

    payload = {
        "id": data.id,
        "user_id": data.user_id,
        "user_login": data.user_login,
        "user_name": data.user_name,
        "game_id": data.game_id,
        "game_name": data.game_name,
        "type": data.type,
        "title": data.title,
        "viewer_count": data.viewer_count,
        "started_at": data.started_at,
        "language": data.language,
        "thumbnail_url": data.thumbnail_url,
        "tag_ids": data.tag_ids,
        "tags": data.tags,
        "is_mature": data.is_mature,
    }
    logger.info(f"Payload {payload}")

    response = client.patch(url=URL_STREAMERS + f"{id}", json=payload)

    assert response.status_code == 404


def test_delete_streamer(client, mongo_mock):
    id = "1111111"

    response = client.delete(url=URL_STREAMERS + f"{id}")

    assert response.status_code == 204
