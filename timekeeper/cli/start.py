"""Start Interface module"""

import click

from timekeeper.model import Times
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
def start(times_model: Times, date: None) -> None:
    """Signals the begining of the clock"""
    if date:
        times_model.register_in(date)
    else:
        times_model.register_in()
        send_notification("Hi Bro!")
        click.echo("Hi bro.")
