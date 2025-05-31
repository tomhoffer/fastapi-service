import logging
from typing import Tuple, List
import psycopg
from psycopg.errors import CheckViolation
from psycopg_pool import AsyncConnectionPool
from src.exceptions import DbUnableToInsertRowException

"""
    This module provides an implementation of the Postgres database interface using psycopg3 and async connection pool.
"""


class DbConnector:
    """
    Connects to the given postgres database
    """
    pool: AsyncConnectionPool = None

    async def init_pool(self, dbname: str, user: str, password: str, host: str, min_size=1, max_size=10):
        try:
            self.pool = AsyncConnectionPool(
                f"dbname={dbname} user={user} password={password} host={host}",
                min_size=min_size,
                max_size=max_size,
                open=True
            )
        except Exception as e:
            logging.critical(f"Could not initialize the connection pool for the PostgreSQL database! {e}")

    async def close_pool(self):
        if self.pool:
            await self.pool.close()


class RecordsDbRepository(DbConnector):

    async def create_record(self, email: str, text: str) -> None:
        async with self.pool.connection() as conn:
            async with conn.cursor() as curs:
                try:
                    await curs.execute(
                        """INSERT INTO records (email, text) VALUES (%s, %s) ON CONFLICT (email)
                        DO UPDATE SET text = excluded.text""",
                        (email, text),
                    )
                except CheckViolation:
                    raise DbUnableToInsertRowException(
                        message=f"Invalid email address provided! Email: {email}"
                    )

    async def get_multiple_records(self, limit: int, offset: int) -> List[Tuple[str, str]]:
        limit = 10 if limit > 10 else limit
        async with self.pool.connection() as conn:
            async with conn.cursor() as curs:
                await curs.execute(
                    """SELECT email, text FROM records ORDER BY email LIMIT %s OFFSET %s""",
                    (limit, offset),
                )
                return await curs.fetchall()

    async def get_record_by_email(self, email: str) -> Tuple[str] | None:
        async with self.pool.connection() as conn:
            async with conn.cursor() as curs:
                await curs.execute(
                    "SELECT text FROM records WHERE email = %s", (email,)
                )
                return await curs.fetchone()

    async def get_record_by_id(self, record_id: int) -> Tuple[int, str, str] | None:
        async with self.pool.connection() as conn:
            async with conn.cursor() as curs:
                await curs.execute(
                    "SELECT id, email, text FROM records WHERE id = %s", (record_id,)
                )
                return await curs.fetchone()

    async def delete_record(self, email: str) -> None:
        async with self.pool.connection() as conn:
            async with conn.cursor() as curs:
                await curs.execute(
                    "DELETE FROM records WHERE email = %s", (email,)
                )
