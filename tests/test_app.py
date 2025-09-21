import pytest
import mongomock
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app, mongo

@pytest.fixture
def client():
    app.config["TESTING"] = True

    # Mocka o MongoDB em memória
    mongo.cx = mongomock.MongoClient()
    mongo.db = mongo.cx["prova_testdb"]

    client = app.test_client()
    yield client
    mongo.db.reports.delete_many({})

def test_placeholder(client):
    response = client.get("/test")
    assert response.status_code == 200