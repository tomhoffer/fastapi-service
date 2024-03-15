import psycopg2
import pytest

from src.config import Config
from src.db import RecordsDbRepository


@pytest.fixture
def records_db():
    return RecordsDbRepository(dbname=Config.get_value('POSTGRES_DB_NAME'), user=Config.get_value('POSTGRES_DB_USER'),
                               password=Config.get_value('POSTGRES_DB_PASSWORD'),
                               host=Config.get_value('POSTGRES_DB_HOST'))


class DbIntegrationTestBase:
    @classmethod
    def setup_class(cls):
        # Set up a connection to the PostgreSQL database
        cls.postgresql_connection = psycopg2.connect(
            dbname=Config.get_value('POSTGRES_DB_NAME'), user=Config.get_value('POSTGRES_DB_USER'),
            password=Config.get_value('POSTGRES_DB_PASSWORD'),
            host=Config.get_value('POSTGRES_DB_HOST'))
        cls.postgresql_connection.set_session(autocommit=True)

    @classmethod
    def teardown_class(cls):
        # Teardown: Close the connection
        cls.postgresql_connection.close()

    def setup_method(self, method):
        # Setup: Create a temporary table
        cursor = self.postgresql_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id SERIAL PRIMARY KEY,
                email domain_email UNIQUE,
            text VARCHAR(100)
            );
        """)

    def teardown_method(self, method):
        # Teardown: Drop the temporary table
        cursor = self.postgresql_connection.cursor()
        cursor.execute("DROP TABLE records")
        self.postgresql_connection.commit()
