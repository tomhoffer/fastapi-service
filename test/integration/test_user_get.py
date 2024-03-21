import pytest


class TestGetUserFromDatabase:

    @pytest.mark.asyncio
    async def test_user_get(
        self, records_db, postgres_setup_and_teardown_async, postgres_async_connection
    ):
        # Test that the correct text is returned for an existing user

        email = "user@gmail.com"
        text = "some text"
        async with postgres_async_connection.cursor() as cursor:
            # Insert fixture user
            await cursor.execute(
                "INSERT INTO records (email, text) VALUES (%s, %s)", (email, text)
            )

            # Get user
            result = await records_db.get_record_by_email(email)

            # Verify obtained user
            assert len(result) == 1
            assert result[0] == text

    @pytest.mark.asyncio
    async def test_user_get_not_exists(
        self, records_db, postgres_setup_and_teardown_async
    ):
        # Test that no user text is returned if the user does not exist

        # Get user
        result = await records_db.get_record_by_email("some_email@gmail.com")

        # Verify obtained user
        assert result is None
