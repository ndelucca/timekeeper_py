"""Stop Interface module"""

import click

from timekeeper.config import Config
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
def stop(conf: Config, date: None) -> None:
    """Signals the end of the clock"""
    if date:
        conf.model.register_out(date)
    else:
        conf.model.register_out()
        send_notification("Bye Bro!")
        click.echo("Bye bro.")
