from timekeeper.database import open_db, register_in, register_out, clear_db


def test_open_db():
    with open_db("test.db") as cursor:
        register_in(cursor)
        register_out(cursor)
        clear_db()
