import pytest
from httpx import AsyncClient
from src.main import app

client = AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_user_post_valid(mocker):
    # API returns the text for given valid email address
    mocker.patch(
        "src.db.RecordsDbRepository.create_record", return_value=None
    )  # Mock the DB creation functionality as it is tested by an integration test
    response = await client.post(
        "/user?email=some_email@gmail.com", json={"text": "some text"}
    )
    assert response.status_code == 200
