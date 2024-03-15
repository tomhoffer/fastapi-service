import pytest
from src.db import RecordsDbRepository
from src.exceptions import DbUnableToInsertRowException
from test.integration.conftest import DbIntegrationTestBase


class TestInsertUserIntoDatabase(DbIntegrationTestBase):

    def test_user_create(self, records_db):
        # Test that user with given email and text was correctly inserted into the database
        email = 'dummy@gmail.com'
        text = 'example text'
        records_db.create_record(email, text)

        # Verify that the row has been inserted
        with self.postgresql_connection.cursor() as cursor:
            cursor.execute("SELECT text FROM records WHERE email = %s", (email,))
            result = cursor.fetchone()
            assert result[0] == text

    def test_user_create_invalid_email(self, records_db):
        # Test that text for user with invalid email was not inserted into the database
        email = 'invalid_email'
        text = 'example text'

        # Assert that exception was raised based on DB constraint violation
        with pytest.raises(DbUnableToInsertRowException):
            records_db.create_record(email, text)

        # Check that row was not inserted into the database
        with self.postgresql_connection.cursor() as cursor:
            cursor.execute("SELECT text FROM records WHERE email = %s", (email,))
            result = cursor.fetchone()
            assert result is None

    def test_existing_user_is_updated(self, records_db):
        # Test that if the user already exists, his text is updated
        email = 'dummy@gmail.com'
        old_text = 'old text'
        new_text = 'new text'

        # Create a record with old text
        with self.postgresql_connection.cursor() as cursor:
            cursor.execute("INSERT INTO records (email, text) VALUES (%s, %s)", (email, old_text))

        # Update the text
        records_db.create_record(email, new_text)

        # Verify that the row has been updated
        with self.postgresql_connection.cursor() as cursor:
            cursor.execute("SELECT text FROM records WHERE email = %s", (email,))
            result = cursor.fetchone()
            assert result[0] == new_text
