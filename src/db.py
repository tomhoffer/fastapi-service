from typing import Tuple
import psycopg2  # TODO change to source distribution

from src.exceptions import DbUnableToInsertRowException


class DbConnector:
    connection = None

    def __init__(self, dbname: str, user: str, password: str, host: str) -> None:
        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        self.connection.set_session(autocommit=True)

    def __del__(self):
        self.connection.close()


class RecordsDbRepository(DbConnector):

    def create_record(self, email: str, text: str) -> None:
        with self.connection.cursor() as curs:
            try:
                return curs.execute(
                    "INSERT INTO records (email, text) VALUES (%s, %s) ON CONFLICT (email) DO UPDATE SET text = excluded.text",
                    (email, text))
            except psycopg2.errors.CheckViolation:
                raise DbUnableToInsertRowException(message="Invalid email address provided!")  # TODO log

    def get_record_by_email(self, email: str) -> Tuple[str] | None:
        with self.connection.cursor() as curs:
            curs.execute("SELECT text FROM records WHERE email = %s", (email,))
            return curs.fetchone()
