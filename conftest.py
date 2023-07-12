import os
from unittest import mock

import mongomock
import pymongo
import pytest
from fastapi.testclient import TestClient
from mongomock.collection import Collection

from database import StreamerDAO
from main import app
from tests.factories import StreamerInFactory


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def db(monkeypatch):
    client = mongomock.MongoClient()
    db = client.get_database("test_db")

    def test_db():
        return db

    monkeypatch.setattr("core.constant_variables.get_db", test_db)


@pytest.fixture()
def streamer_build():
    def streamer(**kwargs):
        return StreamerInFactory.build(**kwargs)

    return streamer


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
