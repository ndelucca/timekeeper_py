"""Database module"""

import datetime
import sqlite3
import logging

from sqlite3 import Cursor

from contextlib import contextmanager

DB_NAME = "timekeeper.db"
TABLE_NAME = "times"
INSERT_STATEMENT = f"INSERT INTO {TABLE_NAME} (`operation`,`date`) VALUES (?, ?);"


def initialize_db(cursor: Cursor) -> None:
    """Creates the timekeeper database and tables"""
    cursor.execute(
        f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
        operation TEXT CHECK( operation IN ('IN','OUT') ) NOT NULL,
        date TIMESTAMP);"""
    )


@contextmanager
def open_db(db_name: str) -> Cursor:
    """Database manager"""
    connection = sqlite3.connect(
        db_name,
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
    )

    try:
        cursor = connection.cursor()
        initialize_db(cursor)
        yield cursor
    except sqlite3.DatabaseError as db_error:
        logging.error(f"Database error: {db_error}")
    finally:
        connection.commit()
        connection.close()


def register_in(cursor: Cursor, date: datetime.datetime) -> None:
    """Registers a user entrance"""
    cursor.execute(INSERT_STATEMENT, ("IN", date))


def register_out(cursor: Cursor, date: datetime.datetime) -> None:
    """Registers a user exit"""
    cursor.execute(INSERT_STATEMENT, ("OUT", date))


def clear_db(cursor: Cursor) -> None:
    """Clears the database tables"""
    cursor.execute(f"DROP TABLE {TABLE_NAME};")


def query_times(cursor: Cursor) -> any:
    """Queries all registers"""

    cursor.execute(f"SELECT `operation`,`date` FROM {TABLE_NAME}")
    fetched_data = cursor.fetchall()

    for row in fetched_data:
        reg_operation = row[0]
        reg_date = row[1]
        print(f"Operation: {reg_operation} Datetime: {reg_date} Type: {type(reg_date)}")
