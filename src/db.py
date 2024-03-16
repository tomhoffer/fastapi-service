import logging
from typing import Tuple, List
from psycopg.errors import CheckViolation
from psycopg_pool import ConnectionPool, PoolTimeout
from src.exceptions import DbUnableToInsertRowException

"""
    This module provides an implementation of the Postgres database interface.
"""


class DbConnector:
    """
    Connects to the given postgres database
    """

    connection_pool: ConnectionPool = None

    def __init__(self, dbname: str, user: str, password: str, host: str) -> None:
        try:
            self.connection_pool = ConnectionPool(
                open=True,
                conninfo=f"dbname={dbname} user={user} password={password} host={host}",
            )
            self.connection_pool.wait()
        except PoolTimeout as e:
            logging.critical(
                f"Could not initialize the connection pool for the PostgreSQL database! {e}"
            )

    def __del__(self):
        self.connection_pool.close()


class RecordsDbRepository(DbConnector):

    def create_record(self, email: str, text: str) -> None:
        with self.connection_pool.connection() as connection:
            with connection.cursor() as curs:
                try:
                    return curs.execute(
                        """INSERT INTO records (email, text) VALUES (%s, %s) ON CONFLICT (email)
                        DO UPDATE SET text = excluded.text""",
                        (email, text),
                    )
                except CheckViolation:
                    raise DbUnableToInsertRowException(
                        message=f"Invalid email address provided! Email: {email}"
                    )

    def get_multiple_records(self, limit: int, offset: int) -> List[Tuple[str, str]]:
        limit = 10 if limit > 10 else limit
        with self.connection_pool.connection() as connection:
            with connection.cursor() as curs:
                curs.execute(
                    """SELECT email, text FROM records ORDER BY email
                LIMIT %s OFFSET %s""",
                    (limit, offset),
                )
                return curs.fetchall()

    def get_record_by_email(self, email: str) -> Tuple[str] | None:
        with self.connection_pool.connection() as connection:
            with connection.cursor() as curs:
                curs.execute("SELECT text FROM records WHERE email = %s", (email,))
                return curs.fetchone()

    def delete_record(self, email: str) -> None:
        with self.connection_pool.connection() as connection:
            with connection.cursor() as curs:
                return curs.execute("DELETE FROM records WHERE email = %s", (email,))
