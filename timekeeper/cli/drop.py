"""Drop Interface module"""

from datetime import datetime

import click

from timekeeper.cli.session import CliSession


@click.command()
@click.option(
    "--date",
    "-d",
    "date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=None,
    help="If used, deletes only registers for this day",
)
@click.pass_obj
def drop(session: CliSession, date: datetime = None) -> None:
    """Deletes registers"""

    if date:
        session.times_model.remove_register(date)
        return

    click.confirm("Are you sure you want to delete all registers?", abort=True)

    session.times_model.clear_db()
