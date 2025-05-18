import pytest
from starlette.testclient import TestClient
from src.main import app


class TestGetMultipleUsersApi:
    client = TestClient(app)

    @pytest.mark.asyncio
    async def test_user_multiple_get_api(self, postgres_async_connection, postgres_setup_and_teardown_async):
        # Happy path test that multiple users can be retrieved

        emails = ["user1@gmail.com", "user2@gmail.com", "user3@gmail.com"]
        texts = ["user1 text", "user2 text", "user3 text"]

        # Insert users directly into DB
        async with postgres_async_connection.cursor() as cursor:
            for email, text in zip(emails, texts):
                await cursor.execute(
                    "INSERT INTO records (email, text) VALUES (%s, %s)",
                    (email, text),
                )

        with TestClient(app) as client:
            response = client.get(f"/users")
            body = response.json()
            assert response.status_code == 200
            assert body == [
                ["user1@gmail.com", "user1 text"],
                ["user2@gmail.com", "user2 text"],
                ["user3@gmail.com", "user3 text"],
            ]

    def test_user_get_multiple_invalid_limit_offset(self):
        # API returns 400 bad request when user provides invalid limit parameter
        response = self.client.get("/users?limit=-10&offset=0")
        assert response.status_code == 400

        # API returns 400 bad request when user provides invalid offset parameter
        response = self.client.get("/users?limit=10&offset=-10")
        assert response.status_code == 400
