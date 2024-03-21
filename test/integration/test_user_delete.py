import pytest


class TestDeleteUserFromDatabase:

    @pytest.mark.asyncio
    async def test_user_delete(
        self, records_db, postgres_async_connection, postgres_setup_and_teardown_async
    ):
        # Test that user with given email was deleted from the database
        email = "dummy@gmail.com"
        text = "example text"

        async with postgres_async_connection.cursor() as cursor:
            # Insert the user to be deleted
            await cursor.execute(
                "INSERT INTO records (email, text) VALUES (%s, %s)", (email, text)
            )

            # Delete the user
            await records_db.delete_record(email)

            # Verify that user was deleted
            await cursor.execute("SELECT * FROM records WHERE email = %s", (email,))
            result = await cursor.fetchone()
            assert result is None
