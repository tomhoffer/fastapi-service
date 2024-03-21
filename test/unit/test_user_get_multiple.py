import pytest
from httpx import AsyncClient
from src.main import app

client = AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_user_get_multiple(mocker):
    # API returns multiple users if they exist
    mocker.patch(
        "src.db.RecordsDbRepository.get_multiple_records",
        return_value=["Result", "Result"],
    )
    response = await client.get("/users")
    body = response.json()
    assert response.status_code == 200
    assert body == ["Result", "Result"]
