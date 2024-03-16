from string import ascii_lowercase

from test.integration.conftest import DbIntegrationTestBase


class TestGetMultipleUsersFromDatabase(DbIntegrationTestBase):

    def test_user_get_multiple(self, records_db):
        # Test that multiple users are returned

        def is_sorted_by_email(lst):
            return all(lst[i][0] <= lst[i + 1][0] for i in range(len(lst) - 1))

        with self.postgresql_connection.cursor() as cursor:
            # Insert fixture users
            emails = [ascii_lowercase[i] + "@gmail.com" for i in range(5)]
            for email in emails:
                cursor.execute(
                    "INSERT INTO records (email, text) VALUES (%s, %s)",
                    (email, "some text"),
                )

            # Get multiple users
            result = records_db.get_multiple_records(limit=10, offset=0)

            # Verify obtained users
            assert len(result) == 5
            assert is_sorted_by_email(result)

    def test_user_get_multiple_limit_reached(self, records_db):
        # Test that maximum of 10 users are returned even if user specifies higher limit

        with self.postgresql_connection.cursor() as cursor:
            # Insert fixture users
            emails = [ascii_lowercase[i] + "@gmail.com" for i in range(15)]
            for email in emails:
                cursor.execute(
                    "INSERT INTO records (email, text) VALUES (%s, %s)",
                    (email, "some text"),
                )

            # Get multiple users
            result = records_db.get_multiple_records(limit=15, offset=0)

            # Verify obtained users
            assert len(result) == 10

    def test_user_get_multiple_limit_offset(self, records_db):
        # Test that limit and offset parameters are respected

        with self.postgresql_connection.cursor() as cursor:
            # Insert fixture users
            emails = [ascii_lowercase[i] + "@gmail.com" for i in range(10)]
            for email in emails:
                cursor.execute(
                    "INSERT INTO records (email, text) VALUES (%s, %s)",
                    (email, "some text"),
                )

            # Get multiple users
            result = records_db.get_multiple_records(limit=5, offset=5)

            # Verify obtained users
            assert len(result) == 5
            assert result == [
                ("f@gmail.com", "some text"),
                ("g@gmail.com", "some text"),
                ("h@gmail.com", "some text"),
                ("i@gmail.com", "some text"),
                ("j@gmail.com", "some text"),
            ]

    def test_user_get_multiple_empty_db(self, records_db):
        # Test that no user is returned when db is empty

        # Get users
        result = records_db.get_multiple_records(limit=10, offset=0)

        # Verify obtained users
        assert len(result) == 0
