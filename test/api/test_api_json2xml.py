from typing import Any
from fastapi.testclient import TestClient
from src.main import app
import xml.etree.ElementTree as ET

client = TestClient(app)


def is_valid_xml(value: Any) -> bool:
    try:
        ET.fromstring(value)
    except ET.ParseError:
        return False
    return True


def test_valid_json():
    response = client.post("/json2xml", json={"foo": "bar"})
    assert response.status_code == 200
    assert is_valid_xml(response.json())


def test_empty_json():
    response = client.post("/json2xml", json={})
    assert response.status_code == 200
    assert is_valid_xml(response.json())


def test_empty_body():
    response = client.post("/json2xml")
    assert response.status_code == 400


def test_invalid_json():
    response = client.post("/json2xml", content="Invalid json")
    assert response.status_code == 400
