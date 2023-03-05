"""Database testing module"""
import os

from timekeeper.database import open_db
from timekeeper.model import (
    CREATE_STATEMENT,
    DROP_STATEMENT,
    INSERT_STATEMENT,
    SELECT_STATEMENT,
)

TEST_DATABASE = "test.db"


def test_open_db():
    """Tests database connections"""
    with open_db("test.db") as cursor:
        cursor.execute(CREATE_STATEMENT)
        cursor.execute(INSERT_STATEMENT, ("IN", "2023-01-01 20:00:00"))
        cursor.execute(INSERT_STATEMENT, ("OUT", "2023-01-01 20:00:00"))
        cursor.execute(SELECT_STATEMENT)
        cursor.execute(DROP_STATEMENT)

    os.remove(TEST_DATABASE)
