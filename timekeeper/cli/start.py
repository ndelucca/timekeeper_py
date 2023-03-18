"""Start Interface module"""

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
def start(session: CliSession, date: None) -> None:
    """Signals the begining of the clock"""
    if date:
        session.times_model.register_in(date)
    else:
        session.times_model.register_in()
        send_notification("Hi Bro!")
        click.echo("Hi bro.")
