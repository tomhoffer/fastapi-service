from starlette.testclient import TestClient
from src.main import app


class TestUserDeleteApi:
    client = TestClient(app)

    def test_user_multiple_get_api(
        self, postgres_connection, postgres_setup_and_teardown
    ):
        # Happy path test that user can be deleted and upon deletion, API returns 404 for provided user

        email = "user@gmail.com"
        text = "some text"

        # Need to use client as a context manager to invoke the @asynccontextmanager lifespan method on the server
        with TestClient(app) as client:
            with postgres_connection.cursor() as cursor:
                # Insert fixture user
                cursor.execute(
                    "INSERT INTO records (email, text) VALUES (%s, %s)", (email, text)
                )

                # Delete user
                response = client.delete(f"/user?email={email}")
                assert response.status_code == 200

                # Get the user
                response = self.client.get(f"/user?email={email}")
                assert response.status_code == 404

    def test_user_delete_without_email(self):
        # Test if API returns 400 Bad Request if user does not provide any email
        response = self.client.delete("/user")
        assert response.status_code == 400
