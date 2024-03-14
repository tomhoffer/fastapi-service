from src.db import RecordsDbRepository
from test.integration.fixtures import DbIntegrationTestBase


class TestDeleteUserFromDatabase(DbIntegrationTestBase):

    def test_user_get(self):
        # Test that the correct is returned for an existing user

        email = 'user@gmail.com'
        text = 'some text'
        with self.postgresql_connection.cursor() as cursor:
            # Insert fixture user
            cursor.execute("INSERT INTO records (email, text) VALUES (%s, %s)", (email, text))

            # Get user
            records_db = RecordsDbRepository(dbname="test_db", user="PM_user", password="PM_password", host="localhost")
            result = records_db.get_record_by_email(email)

            # Verify obtained user
            assert len(result) == 1
            assert result[0] == text

    def test_user_get_not_exists(self):
        # Test that no user text is returned if the user does not exist

        with self.postgresql_connection.cursor() as cursor:
            # Get user
            records_db = RecordsDbRepository(dbname="test_db", user="PM_user", password="PM_password",
                                             host="localhost")
            result = records_db.get_record_by_email('some_email@gmail.com')

            # Verify obtained user
            assert result is None
