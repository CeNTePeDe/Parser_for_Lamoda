import mongomock
import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def mongo_mock(monkeypatch):
    client = mongomock.MongoClient()
    db = client.get_database("CategoryDB")
    col = db.get_collection("test_db")

    def test_db():
        return db

    monkeypatch.setattr("core.constant_variables.db", test_db)
