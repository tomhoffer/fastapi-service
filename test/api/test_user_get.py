from starlette.testclient import TestClient
from src.main import app


class TestGetUserApi:
    client = TestClient(app)

    def test_user_get_api(self, postgres_connection, postgres_setup_and_teardown):
        # Happy path test that the correct text is returned for an existing user

        email = "user@gmail.com"
        text = "some text"

        # Need to use client as a context manager to invoke the @asynccontextmanager lifespan method on the server
        with TestClient(app) as client:
            with postgres_connection.cursor() as cursor:
                # Insert fixture user
                cursor.execute(
                    "INSERT INTO records (email, text) VALUES (%s, %s)", (email, text)
                )

                # Get user
                response = client.get(f"/user?email={email}")
                body = response.json()
                assert response.status_code == 200
                assert body[0] == text

    def test_user_get_without_email(self):
        # API returns 400 Bad Request if user does not provide any email
        response = self.client.get("/user")
        assert response.status_code == 400
