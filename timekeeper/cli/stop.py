"""Stop Interface module"""

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
def stop(times_model: Times, date: None) -> None:
    """Signals the end of the clock"""
    if date:
        times_model.register_out(date)
    else:
        times_model.register_out()
        send_notification("Bye Bro!")
        click.echo("Bye bro.")
