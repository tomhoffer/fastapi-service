from starlette.testclient import TestClient
from src.main import app
from test.integration.conftest import DbIntegrationTestBase


class TestUserDeleteApi(DbIntegrationTestBase):
    client = TestClient(app)

    def test_user_multiple_get_api(self):
        # Happy path test that user can be deleted and upon deletion, API returns 404 for provided user

        email = "user@gmail.com"
        text = "some text"
        with self.postgresql_connection.cursor() as cursor:
            # Insert fixture user
            cursor.execute(
                "INSERT INTO records (email, text) VALUES (%s, %s)", (email, text)
            )

            # Delete user
            response = self.client.delete(f"/user?email={email}")
            assert response.status_code == 200

            # Get the user
            response = self.client.get(f"/user?email={email}")
            assert response.status_code == 404

    def test_user_delete_without_email(self):
        # Test if API returns 400 Bad Request if user does not provide any email
        response = self.client.delete("/user")
        assert response.status_code == 400
