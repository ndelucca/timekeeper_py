"""CLI Interface module"""

import click
from timekeeper.database import open_db, register_in, register_out, query_times
from timekeeper.times import now_rounded


@click.command()
@click.pass_obj
def start(obj: dict):
    """Signals the begining of the clock"""

    with open_db(obj.get("database")) as cursor:
        register_in(cursor, now_rounded())


@click.command()
@click.pass_obj
def stop(obj: dict):
    """Signals the end of the clock"""
    with open_db(obj.get("database")) as cursor:
        register_out(cursor, now_rounded())


@click.command()
@click.pass_obj
def show(obj: dict):
    """Shows current registers"""
    with open_db(obj.get("database")) as cursor:
        query_times(cursor)


@click.group(commands=[start, stop, show])
@click.pass_context
def cli(context=None):
    """CLI Runner group"""

    context.obj = {"database": "timekeeper.db"}


if __name__ == "__main__":
    cli()
