"""Stop Interface module"""

import click

from timekeeper.cli.session import CliSession


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
        click.echo("Bye bro.")
