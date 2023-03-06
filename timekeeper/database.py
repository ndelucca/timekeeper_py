"""Database module"""

import logging
from contextlib import contextmanager
from sqlite3 import PARSE_COLNAMES, PARSE_DECLTYPES, Cursor, DatabaseError, connect


class TimekeeperDatabaseError(DatabaseError):
    """database module exception"""


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
        logging.error(f"Database error: {db_error}")
        raise TimekeeperDatabaseError() from db_error
    finally:
        connection.commit()
        connection.close()
