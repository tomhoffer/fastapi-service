from starlette.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_user_get_invalid_email(mocker):
    mock_db = mocker.Mock()
    mock_db.get_record_by_email.return_value = []
    mocker.patch("src.main.records_db", new=mock_db)
    # API returns 404 if user with given email does not exist
    response = client.get('/user?email=some_email@gmail.com')
    assert response.status_code == 404


def test_user_get_without_email():
    # API returns 400 Bad Request if user does not provide any email
    response = client.get('/user')
    assert response.status_code == 400


def test_valid_user_get(mocker):
    # API returns the text for given valid email address
    mocker.patch('src.db.RecordsDbRepository.get_record_by_email', return_value=["Result"])
    response = client.get('/user?email=some_email@gmail.com')
    body = response.json()
    assert response.status_code == 200
    assert body == ["Result"]
