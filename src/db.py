import logging
from typing import Tuple, List
from psycopg.errors import CheckViolation
from psycopg_pool import PoolTimeout, AsyncConnectionPool
from src.exceptions import DbUnableToInsertRowException

"""
    This module provides an implementation of the Postgres database interface.
"""


class DbConnector:
    """
    Connects to the given postgres database
    """

    async_connection_pool: AsyncConnectionPool = None

    async def init_pool(self, dbname: str, user: str, password: str, host: str):
        try:
            self.async_connection_pool = AsyncConnectionPool(
                open=False,
                conninfo=f"dbname={dbname} user={user} password={password} host={host}",
            )
            await self.async_connection_pool.open()
        except PoolTimeout as e:
            logging.critical(
                f"Could not initialize the connection pool for the PostgreSQL database! {e}"
            )

    async def close_pool(self):
        return await self.async_connection_pool.close()


class RecordsDbRepository(DbConnector):

    async def create_record(self, email: str, text: str) -> None:
        async with self.async_connection_pool.connection() as connection:
            async with connection.cursor() as curs:
                try:
                    return await curs.execute(
                        """INSERT INTO records (email, text) VALUES (%s, %s) ON CONFLICT (email)
                        DO UPDATE SET text = excluded.text""",
                        (email, text),
                    )
                except CheckViolation:
                    raise DbUnableToInsertRowException(
                        message=f"Invalid email address provided! Email: {email}"
                    )

    async def get_multiple_records(
        self, limit: int, offset: int
    ) -> List[Tuple[str, str]]:
        limit = 10 if limit > 10 else limit
        async with self.async_connection_pool.connection() as connection:
            async with connection.cursor() as curs:
                await curs.execute(
                    """SELECT email, text FROM records ORDER BY email LIMIT %s OFFSET %s""",
                    (limit, offset),
                )
                return await curs.fetchall()

    async def get_record_by_email(self, email: str) -> Tuple[str] | None:
        async with self.async_connection_pool.connection() as connection:
            async with connection.cursor() as curs:
                await curs.execute(
                    "SELECT text FROM records WHERE email = %s", (email,)
                )
                return await curs.fetchone()

    async def delete_record(self, email: str) -> None:
        async with self.async_connection_pool.connection() as connection:
            async with connection.cursor() as curs:
                return await curs.execute(
                    "DELETE FROM records WHERE email = %s", (email,)
                )
