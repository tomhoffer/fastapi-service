from starlette.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_user_get_multiple(mocker):
    # API returns multiple users if they exist
    mocker.patch('src.db.RecordsDbRepository.get_multiple_records', return_value=["Result", "Result"])
    response = client.get('/users')
    body = response.json()
    assert response.status_code == 200
    assert body == ["Result", "Result"]


def test_user_get_multiple_invalid_limit_offset():
    # API returns 400 bad request when user provides invalid limit parameter
    response = client.get('/users?limit=-10&offset=0')
    assert response.status_code == 400

    # API returns 400 bad request when user provides invalid offset parameter
    response = client.get('/users?limit=10&offset=-10')
    assert response.status_code == 400
