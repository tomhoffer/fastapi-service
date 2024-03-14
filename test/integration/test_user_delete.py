from src.db import RecordsDbRepository
from test.integration.fixtures import DbIntegrationTestBase


class TestDeleteUserFromDatabase(DbIntegrationTestBase):

    def test_user_delete(self):
        # Test that user with given email was deleted from the database
        email = 'dummy@gmail.com'
        text = 'example text'

        with self.postgresql_connection.cursor() as cursor:
            # Insert the user to be deleted
            cursor.execute("INSERT INTO records (email, text) VALUES (%s, %s)", (email, text))

            # Delete the user
            records_db = RecordsDbRepository(dbname="test_db", user="PM_user", password="PM_password", host="postgres")
            records_db.delete_record(email)

            # Verify that user was deleted
            cursor.execute("SELECT * FROM records WHERE email = %s", (email,))
            result = cursor.fetchone()
            assert result is None
