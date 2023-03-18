"""CLI interface module"""

import click

from timekeeper.cli.drop import drop
from timekeeper.cli.session import CliSession
from timekeeper.cli.show import show
from timekeeper.cli.start import start
from timekeeper.cli.stop import stop


@click.group(commands=[start, stop, show, drop])
@click.version_option(None, "--version", package_name="timekeeper")
@click.pass_context
def cli(context=None) -> None:
    """CLI Runner group"""

    context.obj = CliSession()


if __name__ == "__main__":
    cli()
