import pytest
import pytest_asyncio
import psycopg
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
        min_size=1,
        max_size=10
    )
    yield db
    await db.close_pool()

@pytest_asyncio.fixture
async def postgres_async_connection():
    conn = await psycopg.AsyncConnection.connect(
        dbname=Config.get_value("POSTGRES_DB_NAME"),
        user=Config.get_value("POSTGRES_DB_USER"),
        password=Config.get_value("POSTGRES_DB_PASSWORD"),
        host=Config.get_value("POSTGRES_DB_HOST"),
        autocommit=True,
    )
    yield conn
    await conn.close()

@pytest_asyncio.fixture
async def postgres_setup_and_teardown_async():
    conn = await psycopg.AsyncConnection.connect(
        dbname=Config.get_value("POSTGRES_DB_NAME"),
        user=Config.get_value("POSTGRES_DB_USER"),
        password=Config.get_value("POSTGRES_DB_PASSWORD"),
        host=Config.get_value("POSTGRES_DB_HOST"),
        autocommit=True,
    )
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
    yield
    # Teardown: Drop the temporary table
    async with conn.cursor() as cursor:
        await cursor.execute("DROP TABLE records")
    await conn.close()
