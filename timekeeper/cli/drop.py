"""Drop Interface module"""

import click

from timekeeper.model import Times


@click.command()
@click.pass_obj
def drop(times_model: Times) -> None:
    """Destroys all registers"""
    times_model.clear_db()
