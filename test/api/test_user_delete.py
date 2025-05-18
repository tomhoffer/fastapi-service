import pytest
from starlette.testclient import TestClient
from src.main import app


class TestUserDeleteApi:
    client = TestClient(app)

    @pytest.mark.asyncio
    async def test_user_multiple_get_api(self, postgres_async_connection, postgres_setup_and_teardown_async):
        email = "user@gmail.com"
        text = "some text"
        # Insert user directly into DB
        async with postgres_async_connection.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO records (email, text) VALUES (%s, %s)", (email, text)
            )

        with TestClient(app) as client:
            response = client.delete(f"/user?email={email}")
            assert response.status_code == 200
            response = self.client.get(f"/user?email={email}")
            assert response.status_code == 404

    def test_user_delete_without_email(self):
        # Test if API returns 400 Bad Request if user does not provide any email
        response = self.client.delete("/user")
        assert response.status_code == 400
