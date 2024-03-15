from test.integration.conftest import DbIntegrationTestBase


class TestDeleteUserFromDatabase(DbIntegrationTestBase):

    def test_user_get(self, records_db):
        # Test that the correct is returned for an existing user

        email = 'user@gmail.com'
        text = 'some text'
        with self.postgresql_connection.cursor() as cursor:
            # Insert fixture user
            cursor.execute("INSERT INTO records (email, text) VALUES (%s, %s)", (email, text))

            # Get user
            result = records_db.get_record_by_email(email)

            # Verify obtained user
            assert len(result) == 1
            assert result[0] == text

    def test_user_get_not_exists(self, records_db):
        # Test that no user text is returned if the user does not exist

        with self.postgresql_connection.cursor() as cursor:
            # Get user
            result = records_db.get_record_by_email('some_email@gmail.com')

            # Verify obtained user
            assert result is None
