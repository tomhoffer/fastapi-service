import psycopg2


class DbIntegrationTestBase:
    @classmethod
    def setup_class(cls):
        # Set up a connection to the PostgreSQL database
        cls.postgresql_connection = psycopg2.connect(
            "dbname=test_db user=PM_user host=localhost password=PM_password")
        cls.postgresql_connection.set_session(autocommit=True)

    @classmethod
    def teardown_class(cls):
        # Teardown: Close the connection
        cls.postgresql_connection.close()

    def setup_method(self, method):
        # Setup: Create a temporary table
        cursor = self.postgresql_connection.cursor()
        cursor.execute("""
            CREATE TABLE records (
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
