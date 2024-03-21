import pytest
from httpx import AsyncClient
from src.main import app

client = AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_valid_user_delete(mocker):
    # Test valid user deletion
    mocker.patch(
        "src.db.RecordsDbRepository.delete_record", return_value=None
    )  # Mock the DB deletion functionality as it is tested by an integration test
    response = await client.delete("/user?email=some_email@gmail.com")
    assert response.status_code == 200
