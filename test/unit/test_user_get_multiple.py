from starlette.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_user_get_multiple(mocker):
    # API returns multiple users if they exist
    mocker.patch(
        "src.db.RecordsDbRepository.get_multiple_records",
        return_value=["Result", "Result"],
    )
    response = client.get("/users")
    body = response.json()
    assert response.status_code == 200
    assert body == ["Result", "Result"]
