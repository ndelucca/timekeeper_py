"""Database module"""

from datetime import datetime
from functools import partial
from typing import List
from timekeeper.database import open_db
from timekeeper.times import now_rounded

TABLE_NAME = "times"


class TimekeeperModelError(Exception):
    """database module exception"""


class Times:
    """Represents the timekeeping table model"""

    database: str
    connection: callable
    table: str = TABLE_NAME

    def __init__(self, database):
        self.database = database
        self.connection = partial(open_db, database)

        self.initialize_db()

    def initialize_db(self) -> None:
        """Creates the timekeeper database and tables"""
        with self.connection() as cursor:
            try:
                cursor.execute(
                    f"""CREATE TABLE IF NOT EXISTS `{self.table}` (
                    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                    operation TEXT CHECK( operation IN ('IN','OUT') ) NOT NULL,
                    date TIMESTAMP);"""
                )
            except Exception as db_error:
                raise TimekeeperModelError from db_error

    def register_row(self, operation: str, date: datetime) -> None:
        """Registers a row"""

        with self.connection() as cursor:
            try:
                cursor.execute(
                    f"INSERT INTO `{self.table}` (`operation`,`date`) VALUES (?, ?);",
                    (operation, date),
                )
            except Exception as db_error:
                raise TimekeeperModelError from db_error

    def register_in(self, date: datetime = now_rounded()) -> None:
        """Registers a user entrance"""
        self.register_row("IN", date)

    def register_out(self, date: datetime = now_rounded()) -> None:
        """Registers a user exit"""
        self.register_row("OUT", date)

    def clear_db(self) -> None:
        """Clears the database tables"""
        with self.connection() as cursor:
            try:
                cursor.execute(f"DROP TABLE `{self.table}`;")
            except Exception as db_error:
                raise TimekeeperModelError from db_error

    def query_all(self) -> List[list]:
        """Queries all registers"""

        with self.connection() as cursor:
            try:
                cursor.execute(f"SELECT `operation`,`date` FROM `{self.table}`;")
                fetched_data = cursor.fetchall()
                return fetched_data
            except Exception as db_error:
                raise TimekeeperModelError from db_error

    def query_day(self, day: datetime) -> List[datetime]:
        """Returns all registers related to a single day"""
        pass
