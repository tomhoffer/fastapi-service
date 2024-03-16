from starlette.testclient import TestClient
from src.main import app
from test.integration.conftest import DbIntegrationTestBase


class TestGetUserApi(DbIntegrationTestBase):
    client = TestClient(app)

    def test_user_get_api(self):
        # Happy path test that the correct text is returned for an existing user

        email = "user@gmail.com"
        text = "some text"
        with self.postgresql_connection.cursor() as cursor:
            # Insert fixture user
            cursor.execute(
                "INSERT INTO records (email, text) VALUES (%s, %s)", (email, text)
            )

            # Get user
            response = self.client.get(f"/user?email={email}")
            body = response.json()
            assert response.status_code == 200
            assert body[0] == text

    def test_user_get_without_email(self):
        # API returns 400 Bad Request if user does not provide any email
        response = self.client.get("/user")
        assert response.status_code == 400
