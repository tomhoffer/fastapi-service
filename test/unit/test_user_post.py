from starlette.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_user_post_valid(mocker):
    # API returns the text for given valid email address
    mocker.patch(
        "src.db.RecordsDbRepository.create_record", return_value=None
    )  # Mock the DB creation functionality as it is tested by an integration test
    response = client.post(
        "/user?email=some_email@gmail.com", json={"text": "some text"}
    )
    assert response.status_code == 200
