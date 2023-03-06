"""Database module"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import partial
from typing import List

from timekeeper.database import open_db
from timekeeper.times import now_rounded

TABLE_NAME = "times"
DATE_FMT = "%Y-%m-%d"
TIME_FMT = "%H:%M"

class TimekeeperModelError(Exception):
    """database module exception"""


@dataclass
class Day:
    """Represents a days work time"""

    in_dt: datetime
    out_dt: datetime
    hours: timedelta

    @classmethod
    def from_dict(cls, times: dict) -> "Day":
        """Creates a Day from a dict with multiple IN and OUT registers"""

        ins: list = times.get("IN")
        outs: list = times.get("OUT")

        if len(ins) != len(outs):
            logging.warning(f"IN {ins} != OUT {outs}")

        delta: timedelta = timedelta()
        for rin,rout in zip(ins,outs):
            delta+=rout-rin

        return Day(in_dt=ins[0], out_dt=ins[0]+delta, hours=delta)

    def __str__(self) -> str:

        return "{day}: {time_in} - {time_out}".format(
            day=self.in_dt.strftime(DATE_FMT),
            time_in=self.in_dt.strftime(TIME_FMT),
            time_out=self.out_dt.strftime(TIME_FMT),
        )

    def tuple(self) -> tuple:
        return (
            self.in_dt.strftime(DATE_FMT),
            self.in_dt.strftime(TIME_FMT),
            self.out_dt.strftime(TIME_FMT),
            self.hours
        )



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

    def query_day(self, day: datetime) -> Day:
        """Returns all registers related to a single day"""

        with self.connection() as cursor:
            try:
                cursor.execute(
                    f"""SELECT `operation`,GROUP_CONCAT(`date`) FROM `{self.table}`
                WHERE `date` LIKE ? GROUP BY `operation`;""",
                    (f"%{day.date()}%",),
                )
                fetched_data = cursor.fetchall()

                if not fetched_data:
                    return []

            except Exception as db_error:
                raise TimekeeperModelError from db_error

        days = {}
        for operation, times in fetched_data:
            days[operation] = [
                datetime.fromisoformat(time) for time in times.split(",")
            ]

        return Day.from_dict(days)
