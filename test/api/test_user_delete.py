from starlette.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_user_delete_without_email():
    # Test if API returns 400 Bad Request if user does not provide any email
    response = client.delete('/user')
    assert response.status_code == 400


def test_valid_user_delete(mocker):
    # Test valid user deletion
    mocker.patch('src.db.RecordsDbRepository.delete_record',
                 return_value=None)  # Mock the DB deletion functionality as it is tested by an integration test
    response = client.delete('/user?email=some_email@gmail.com')
    assert response.status_code == 200
