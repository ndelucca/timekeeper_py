"""Drop Interface module"""

import click

from timekeeper.cli.session import CliSession


@click.command()
@click.pass_obj
def drop(session: CliSession) -> None:
    """Destroys all registers"""
    session.times_model.clear_db()
