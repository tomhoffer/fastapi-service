import asyncio

import pytest
from httpx import AsyncClient
from src.main import app

client = AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_user_get_invalid_email(mocker):
    future = asyncio.Future()
    future.set_result([])
    mock_db = mocker.Mock()
    mock_db.get_record_by_email.return_value = future
    mocker.patch("src.main.records_db", new=mock_db)
    # API returns 404 if user with given email does not exist
    response = await client.get("/user?email=some_email@gmail.com")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_valid_user_get(mocker):
    # API returns the text for given valid email address
    mocker.patch(
        "src.db.RecordsDbRepository.get_record_by_email", return_value=["Result"]
    )
    response = await client.get("/user?email=some_email@gmail.com")
    body = response.json()
    assert response.status_code == 200
    assert body == ["Result"]
