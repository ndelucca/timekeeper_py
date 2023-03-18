"""Database testing module"""
import os

from timekeeper.database import open_db

TEST_DATABASE = "test_database.db"
TEST_TABLE = "test_times"

CREATE_STATEMENT = f"""CREATE TABLE IF NOT EXISTS `{TEST_TABLE}` (
                    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                    operation TEXT CHECK( operation IN ('IN','OUT') ) NOT NULL,
                    date TIMESTAMP);"""
INSERT_STATEMENT = f"INSERT INTO `{TEST_TABLE}` (`operation`,`date`) VALUES (?, ?);"
DROP_STATEMENT = f"DROP TABLE `{TEST_TABLE}`;"
SELECT_STATEMENT = f"SELECT `operation`,`date` FROM `{TEST_TABLE}`;"


def test_open_db():
    """Tests database connections"""
    with open_db(TEST_DATABASE) as cursor:
        cursor.execute(CREATE_STATEMENT)
        cursor.execute(INSERT_STATEMENT, ("IN", "2023-01-01 20:00:00"))
        cursor.execute(INSERT_STATEMENT, ("OUT", "2023-01-01 20:00:00"))
        cursor.execute(SELECT_STATEMENT)
        cursor.execute(DROP_STATEMENT)

    os.remove(TEST_DATABASE)
