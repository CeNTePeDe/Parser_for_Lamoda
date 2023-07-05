import logging

from tests.factories import CategoryFactory

logger = logging.getLogger(__name__)

URL = "http://localhost:8000/api/categories/"


def test_get_categories(client, mongo_mock):
    response = client.get(url=URL)
    assert response.status_code == 200


def test_create_category(client, mongo_mock):
    data = CategoryFactory.build()
    payload = {"category": data.category}
    logger.info(f"payload is {payload}")

    response = client.post(url=URL, json=payload)
    assert response.status_code == 201


def test_get_category(client, mongo_mock):
    category = "test_category"
    response = client.get(url=URL + f"{category}")
    assert response.status_code == 200


def test_get_invalid_category(client, mongo_mock):
    category = "invalid_category"
    response = client.get(url=URL + f"{category}")
    assert response.status_code == 404


def test_update_category(client, mongo_mock):
    category = "new_test_category"

    new_data = {
        "category": "new_category",
    }
    response = client.put(url=URL + f"{category}", json=new_data)
    assert response.status_code == 200


def test_delete_category(client):
    category = "new_category"
    response = client.delete(url=URL + f"{category}")
    assert response.status_code == 204
