from unittest import mock

import mongomock
import pytest
from fastapi.testclient import TestClient
from mongomock.collection import Collection

from database import StreamerDAO
from main import app
from tests.factories import CategoryFactory, ProductFactory, StreamerInFactory


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def test_db():
    client = mongomock.MongoClient()
    db = client.get_database("test_db")
    return db


@pytest.fixture()
def streamer_build():
    def streamer(**kwargs):
        return StreamerInFactory.build(**kwargs)

    return streamer


@pytest.fixture()
def category_build():
    def category(**kwargs):
        return CategoryFactory.build(**kwargs)

    return category


@pytest.fixture()
def product_build():
    def product(**kwargs):
        return ProductFactory.build(**kwargs)

    return product


@pytest.fixture()
def streamer():
    streamer = dict(StreamerInFactory.build())
    return streamer


@pytest.fixture()
def dao_streamer_test():
    mock_collection = mock.MagicMock(Collection)
    dao = StreamerDAO()
    dao.collection = mock_collection
    yield dao
