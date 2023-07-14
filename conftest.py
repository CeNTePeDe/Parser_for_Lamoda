import mongomock
import pytest
from fastapi.testclient import TestClient

from main import app
from tests.factories import StreamerInFactory


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
def streamer():
    streamer = dict(StreamerInFactory.build())
    return streamer
