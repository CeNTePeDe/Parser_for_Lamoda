import logging

from core.constant_variables import URL_CATEGORIES
from tests.factories import CategoryFactory

logger = logging.getLogger(__name__)


def test_get_categories(client, test_db):
    response = client.get(url=URL_CATEGORIES)

    assert response.status_code == 200


def test_create_category(client, test_db):
    data = CategoryFactory.build()
    payload = {"category": data.category}
    logger.info(f"payload is {payload}")

    response = client.post(url=URL_CATEGORIES, json=payload)

    assert response.status_code == 201


def test_get_category(client, test_db):
    category = "test_category"

    response = client.get(url=URL_CATEGORIES + f"{category}")

    assert response.status_code == 200


def test_get_invalid_category(client, test_db):
    category = "invalid_category"

    response = client.get(url=URL_CATEGORIES + f"{category}")

    assert response.status_code == 404


def test_update_category(client, test_db):
    category = "test_category"

    new_data = {
        "category": "new_category",
    }
    response = client.put(url=URL_CATEGORIES + f"{category}", json=new_data)

    assert response.status_code == 200


def test_delete_category(client):
    category = "new_category"

    response = client.delete(url=URL_CATEGORIES + f"{category}")

    assert response.status_code == 204
