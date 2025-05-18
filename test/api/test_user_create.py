import pytest
from starlette.testclient import TestClient
from src.main import app

class TestCreateUserApi:
    client = TestClient(app)

    @pytest.mark.asyncio
    async def test_user_post_api(self, postgres_async_connection, postgres_setup_and_teardown_async):
        # Happy path test that the user can be created and retrieved

        email = "user@gmail.com"
        text = "some text"

        # Need to use client as a context manager to invoke the @asynccontextmanager lifespan method on the server
        with TestClient(app) as client:
            response = client.post(f"/user?email={email}", json={"text": text})
            assert response.status_code == 200

        # Verify user was created in DB
        async with postgres_async_connection.cursor() as cursor:
            await cursor.execute("SELECT text FROM records WHERE email = %s", (email,))
            result = await cursor.fetchone()
            assert result[0] == text

    def test_user_post_without_email(self):
        # API returns 400 Bad Request if user does not provide any email
        response = self.client.post("/user", json={"text": "some text"})
        assert response.status_code == 400

    def test_user_post_invalid_payload(self):
        # API returns 400 Bad Request if user provides invalid payload
        response = self.client.post("/user", json={})
        assert response.status_code == 400
