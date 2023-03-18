"""Database testing module"""
import os
from datetime import datetime

from timekeeper.model import Times

TEST_DATABASE = "test.db"
TEST_DATE = datetime(2023, 4, 8)


def test_times_instance():
    """Tests database connections"""

    times = Times(TEST_DATABASE)
    times.register_in()
    times.register_out()
    times.query_all()
    times.register_in(TEST_DATE)
    times.remove_register(TEST_DATE)
    times.clear_db()

    os.remove(TEST_DATABASE)
