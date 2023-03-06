"""CLI Interface module"""

from datetime import datetime

import click
from tabulate import tabulate

from timekeeper.model import Times


@click.command()
@click.pass_obj
def start(times_model: Times):
    """Signals the begining of the clock"""
    times_model.register_in()


@click.command()
@click.pass_obj
def stop(times_model: Times):
    """Signals the end of the clock"""
    times_model.register_out()


@click.command()
@click.pass_obj
def show(times_model: Times):
    """Shows current registers"""

    table = tabulate(
        times_model.query_all(), headers=["Operation", "Date"], tablefmt="fancy_grid"
    )
    print(table)


@click.command()
@click.pass_obj
def today(times_model: Times):
    """Shows current registers"""

    day = times_model.query_day(datetime.now())
    table = tabulate(
        [day.tuple(),], headers=["Day", "In", "Out", "Total"], tablefmt="fancy_grid"
    )
    print(table)

@click.command()
@click.pass_obj
def drop(times_model: Times):
    """Destroys all registers"""
    times_model.clear_db()


@click.group(commands=[start, stop, show, drop, today])
@click.version_option(None, "--version", package_name="timekeeper")
@click.option(
    "--database",
    "-db",
    "database",
    default="timekeeper.db",
    type=str,
    help="Database filename",
)
@click.pass_context
def cli(context=None, database: str = None):
    """CLI Runner group"""

    context.obj = Times(database)


if __name__ == "__main__":
    cli()
