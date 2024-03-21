import psycopg
import pytest
import pytest_asyncio

from src.config import Config
from src.db import RecordsDbRepository


@pytest_asyncio.fixture
async def records_db():
    db = RecordsDbRepository()
    await db.init_pool(
        dbname=Config.get_value("POSTGRES_DB_NAME"),
        user=Config.get_value("POSTGRES_DB_USER"),
        password=Config.get_value("POSTGRES_DB_PASSWORD"),
        host=Config.get_value("POSTGRES_DB_HOST"),
    )
    yield db

    await db.close_pool()


@pytest_asyncio.fixture
async def postgres_async_connection():
    # Connect to the PostgreSQL database
    conn = await psycopg.AsyncConnection.connect(
        dbname=Config.get_value("POSTGRES_DB_NAME"),
        user=Config.get_value("POSTGRES_DB_USER"),
        password=Config.get_value("POSTGRES_DB_PASSWORD"),
        host=Config.get_value("POSTGRES_DB_HOST"),
        autocommit=True,
    )

    yield conn

    # Close the connection after all tests have run
    await conn.close()


@pytest.fixture
def postgres_connection():
    # Connect to the PostgreSQL database
    conn = psycopg.connect(
        dbname=Config.get_value("POSTGRES_DB_NAME"),
        user=Config.get_value("POSTGRES_DB_USER"),
        password=Config.get_value("POSTGRES_DB_PASSWORD"),
        host=Config.get_value("POSTGRES_DB_HOST"),
        autocommit=True,
    )

    yield conn

    # Close the connection after all tests have run
    conn.close()


@pytest_asyncio.fixture
async def postgres_setup_and_teardown_async():
    # Set up a connection to the PostgreSQL database
    conn = await psycopg.AsyncConnection.connect(
        dbname=Config.get_value("POSTGRES_DB_NAME"),
        user=Config.get_value("POSTGRES_DB_USER"),
        password=Config.get_value("POSTGRES_DB_PASSWORD"),
        host=Config.get_value("POSTGRES_DB_HOST"),
    )
    await conn.set_autocommit(True)

    # Setup: Create a temporary table
    async with conn.cursor() as cursor:
        await cursor.execute(
            """
                    CREATE TABLE IF NOT EXISTS records (
                        id SERIAL PRIMARY KEY,
                        email domain_email UNIQUE,
                    text VARCHAR(100)
                    );
                """
        )

    # Test execution
    yield

    # Teardown: Drop the temporary table
    async with conn.cursor() as cursor:
        await cursor.execute("DROP TABLE records")

    # Teardown: Close the connection
    await conn.close()


@pytest.fixture()
def postgres_setup_and_teardown():
    # Set up a connection to the PostgreSQL database
    conn = psycopg.connect(
        dbname=Config.get_value("POSTGRES_DB_NAME"),
        user=Config.get_value("POSTGRES_DB_USER"),
        password=Config.get_value("POSTGRES_DB_PASSWORD"),
        host=Config.get_value("POSTGRES_DB_HOST"),
        autocommit=True,
    )

    # Setup: Create a temporary table
    with conn.cursor() as cursor:
        cursor.execute(
            """
                    CREATE TABLE IF NOT EXISTS records (
                        id SERIAL PRIMARY KEY,
                        email domain_email UNIQUE,
                    text VARCHAR(100)
                    );
                """
        )

    # Test execution
    yield

    # Teardown: Drop the temporary table
    with conn.cursor() as cursor:
        cursor.execute("DROP TABLE records")

    # Teardown: Close the connection
    conn.close()
