"""Stop Interface module"""

import click

from timekeeper.cli.session import CliSession
from timekeeper.notification import send_notification


@click.command()
@click.option(
    "--date",
    "-d",
    "date",
    type=click.DateTime(formats=["%Y-%m-%d %H:%M"]),
    default=None,
)
@click.pass_obj
def stop(session: CliSession, date: None) -> None:
    """Signals the end of the clock"""
    if date:
        session.times_model.register_out(date)
    else:
        session.times_model.register_out()
        send_notification("Bye Bro!")
        click.echo("Bye bro.")
