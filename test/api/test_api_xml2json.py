import json
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_valid_xml():
    response = client.post("/xml2json", content='<ITEM type="object" />')
    assert response.status_code == 200
    json.loads(response.json())


def test_empty_body():
    response = client.post("/xml2json")
    assert response.status_code == 400


def test_invalid_xml():
    response = client.post("/xml2json", content="Invalid XML")
    assert response.status_code == 400
