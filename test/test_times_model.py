"""Database testing module"""
import os

from timekeeper.model import Times

TEST_DATABASE = "test.db"


def test_times_instance():
    """Tests database connections"""

    times = Times(TEST_DATABASE)
    times.register_in()
    times.register_out()
    times.query_all()
    times.clear_db()

    os.remove(TEST_DATABASE)
