"""CLI interface module"""
import os

import click

from timekeeper.cli.drop import drop
from timekeeper.cli.show import show
from timekeeper.cli.start import start
from timekeeper.cli.stop import stop
from timekeeper.model import Times


@click.group(commands=[start, stop, show, drop])
@click.version_option(None, "--version", package_name="timekeeper")
@click.pass_context
def cli(context=None) -> None:
    """CLI Runner group"""

    home = os.path.expanduser("~")
    database = os.path.join(home, "timekeeper.db")

    context.obj = Times(database)


if __name__ == "__main__":
    cli()
