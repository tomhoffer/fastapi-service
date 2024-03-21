import pytest
from src.exceptions import DbUnableToInsertRowException


class TestInsertUserIntoDatabase:

    @pytest.mark.asyncio
    async def test_user_create(
        self, records_db, postgres_async_connection, postgres_setup_and_teardown_async
    ):
        # Test that user with given email and text was correctly inserted into the database
        email = "dummy@gmail.com"
        text = "example text"
        await records_db.create_record(email, text)

        # Verify that the row has been inserted
        async with postgres_async_connection.cursor() as cursor:
            await cursor.execute("SELECT text FROM records WHERE email = %s", (email,))
            result = await cursor.fetchone()
            assert result[0] == text

    @pytest.mark.asyncio
    async def test_user_create_invalid_email(
        self, records_db, postgres_async_connection, postgres_setup_and_teardown_async
    ):
        # Test that text for user with invalid email was not inserted into the database
        email = "invalid_email"
        text = "example text"

        # Assert that exception was raised based on DB constraint violation
        with pytest.raises(DbUnableToInsertRowException):
            await records_db.create_record(email, text)

        # Check that row was not inserted into the database
        async with postgres_async_connection.cursor() as cursor:
            await cursor.execute("SELECT text FROM records WHERE email = %s", (email,))
            result = await cursor.fetchone()
            assert result is None

    @pytest.mark.asyncio
    async def test_existing_user_is_updated(
        self, records_db, postgres_async_connection, postgres_setup_and_teardown_async
    ):
        # Test that if the user already exists, his text is updated
        email = "dummy@gmail.com"
        old_text = "old text"
        new_text = "new text"

        # Create a record with old text
        async with postgres_async_connection.cursor() as cursor:
            await cursor.execute(
                "INSERT INTO records (email, text) VALUES (%s, %s)", (email, old_text)
            )

        # Update the text
        await records_db.create_record(email, new_text)

        # Verify that the row has been updated
        async with postgres_async_connection.cursor() as cursor:
            await cursor.execute("SELECT text FROM records WHERE email = %s", (email,))
            result = await cursor.fetchone()
            assert result[0] == new_text
