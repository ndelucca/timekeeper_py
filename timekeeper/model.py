"""Database module"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import partial
from typing import List, Callable

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
        for rin, rout in zip(ins, outs):
            delta += rout - rin

        return Day(in_dt=ins[0], out_dt=ins[0] + delta, hours=delta)

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
            self.hours,
        )

    def day_str(self) -> str:
        return self.in_dt.strftime(DATE_FMT)

    def time_in_str(self) -> str:
        return self.in_dt.strftime(TIME_FMT)

    def time_out_str(self) -> str:
        return self.out_dt.strftime(TIME_FMT)


class Times:
    """Represents the timekeeping table model"""

    database: str
    connection: Callable
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

    def query_all(self, filters: dict = None) -> List[list]:
        """Queries all registers"""

        if filters is None:
            filters = {}

        where = []
        binds = []

        if filters.get("date_from"):
            where.append(f"`date` >= ?")
            binds.append(filters.get("date_from"))

        if filters.get("date_to"):
            where.append(f"`date` <= ?")
            binds.append(filters.get("date_to"))

        with self.connection() as cursor:
            query = f"SELECT `operation`,`date` FROM `{self.table}`"
            if where:
                query += f"WHERE {' AND '.join(where)}"

            try:
                cursor.execute(query, binds)
                fetched_data = cursor.fetchall()
                return fetched_data
            except Exception as db_error:
                raise TimekeeperModelError from db_error

    def query_days(self, filters: dict = None) -> List[Day]:
        """Returns filtered registers as days"""
        query = self.query_all(filters=filters)

        days = {}
        for reg_operation, reg_date in query:
            day_key = reg_date.strftime("%Y-%m-%d")

            if not days.get(day_key):
                days[day_key] = {}

            if not days[day_key].get(reg_operation):
                days[day_key][reg_operation] = []

            days[day_key][reg_operation].append(reg_date)

        return [Day.from_dict(day) for day in days.values()]
