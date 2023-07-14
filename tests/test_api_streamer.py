from core.constant_variables import URL_STREAMERS, URL_STREAMERS_PARSE
from database import StreamerDAO

dao_streamer = StreamerDAO()


def test_get_streamers(client):
    response = client.get(url=URL_STREAMERS)

    assert response.status_code == 200
    assert len(response.json()) == len(dao_streamer.get_all_items())


def test_parse_streamer(client):
    response = client.post(url=URL_STREAMERS_PARSE)

    assert response.status_code == 200



def test_create_streamer(test_db, client, streamer):
    response = client.post(url=URL_STREAMERS, json=streamer)

    assert response.status_code == 201
    assert response.json()["id"] == streamer["id"]
    assert response.json()["user_id"] == streamer["user_id"]
    assert response.json()["game_id"] == streamer["game_id"]
    assert response.json()["viewer_count"] == streamer["viewer_count"]


def test_get_streamer(test_db, client, streamer):
    id = "id_0"

    response = client.get(url=URL_STREAMERS + f"{id}")

    assert response.status_code == 200
    assert response.json()["id"] == "id_0"
    assert response.json()["user_id"] == "user_id_0"
    assert response.json()["title"] == "title_0"


def test_get_invalid_streamer(test_db, client):
    id = "invalid_id"
    response = client.get(url=URL_STREAMERS + f"{id}")

    assert response.status_code == 404


def test_update_streamer(test_db, streamer, streamer_build, client):
    new_streamer = streamer_build()
    id = "id_0"
    response = client.patch(url=URL_STREAMERS + f"{id}", json=new_streamer.dict())

    assert response.status_code == 200


def test_delete_streamer(test_db, client, streamer):
    id = streamer["id"]
    response = client.delete(url=URL_STREAMERS + f"{id}")

    assert response.status_code == 205
