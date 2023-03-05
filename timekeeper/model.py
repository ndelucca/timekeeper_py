"""Database module"""

from datetime import datetime
from functools import partial

from timekeeper.database import open_db
from timekeeper.times import now_rounded

TABLE_NAME = "times"
INSERT_STATEMENT = f"INSERT INTO {TABLE_NAME} (`operation`,`date`) VALUES (?, ?);"
DROP_STATEMENT = f"DROP TABLE {TABLE_NAME}"
SELECT_STATEMENT = f"SELECT `operation`,`date` FROM {TABLE_NAME}"
CREATE_STATEMENT = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    operation TEXT CHECK( operation IN ('IN','OUT') ) NOT NULL,
    date TIMESTAMP);"""


class Times:
    """Represents the timekeeping table model"""

    database: str
    connection: callable

    def __init__(self, database):
        self.database = database
        self.connection = partial(open_db, database)

        self.initialize_db()

    def initialize_db(self) -> None:
        """Creates the timekeeper database and tables"""
        with self.connection() as cursor:
            cursor.execute(CREATE_STATEMENT)

    def register_in(self, date: datetime = now_rounded()):
        """Registers a user entrance"""
        with self.connection() as cursor:
            cursor.execute(INSERT_STATEMENT, ("IN", date))

    def register_out(self, date: datetime = now_rounded()) -> None:
        """Registers a user exit"""
        with self.connection() as cursor:
            cursor.execute(INSERT_STATEMENT, ("OUT", date))

    def clear_db(self) -> None:
        """Clears the database tables"""
        with self.connection() as cursor:
            cursor.execute(DROP_STATEMENT)

    def query_times(self, filters=None) -> list[list]:
        """Queries all registers"""
        with self.connection() as cursor:
            cursor.execute(SELECT_STATEMENT)
            fetched_data = cursor.fetchall()

        return fetched_data
