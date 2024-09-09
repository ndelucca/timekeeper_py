"""Database module"""

import logging
from contextlib import contextmanager
import sqlite3
import datetime
from sqlite3 import PARSE_COLNAMES, PARSE_DECLTYPES, Cursor, DatabaseError, connect


class TimekeeperDatabaseError(DatabaseError):
    """database module exception"""

def adapt_date_iso(val):
    """Adapt datetime.date to ISO 8601 date."""
    return val.isoformat()

def adapt_datetime_iso(val):
    """Adapt datetime.datetime to timezone-naive ISO 8601 date."""
    return val.isoformat()

def adapt_datetime_epoch(val):
    """Adapt datetime.datetime to Unix timestamp."""
    return int(val.timestamp())

sqlite3.register_adapter(datetime.date, adapt_date_iso)
sqlite3.register_adapter(datetime.datetime, adapt_datetime_iso)
sqlite3.register_adapter(datetime.datetime, adapt_datetime_epoch)

def convert_date(val):
    """Convert ISO 8601 date to datetime.date object."""
    return datetime.date.fromisoformat(val.decode())

def convert_datetime(val):
    """Convert ISO 8601 datetime to datetime.datetime object."""
    return datetime.datetime.fromisoformat(val.decode())

def convert_timestamp(val):
    """Convert Unix epoch timestamp to datetime.datetime object."""
    return datetime.datetime.fromtimestamp(int(val))

sqlite3.register_converter("date", convert_date)
sqlite3.register_converter("datetime", convert_datetime)
sqlite3.register_converter("timestamp", convert_timestamp)

@contextmanager
def open_db(db_name: str) -> Cursor:
    """Database manager"""
    connection = connect(
        db_name,
        detect_types=PARSE_DECLTYPES | PARSE_COLNAMES,
    )

    try:
        cursor = connection.cursor()
        yield cursor
    except DatabaseError as db_error:
        logging.error("Database error: %s", db_error)
        raise TimekeeperDatabaseError() from db_error
    finally:
        connection.commit()
        connection.close()
