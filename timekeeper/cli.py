"""CLI Interface module"""

from datetime import datetime
from functools import partial

import click
from tabulate import tabulate

from timekeeper.model import Times


def header_style(text: str) -> str:
    partial_func = partial(click.style, fg="green", bold=True)
    return partial_func(text)


@click.command()
@click.pass_obj
def start(times_model: Times) -> None:
    """Signals the begining of the clock"""
    times_model.register_in()


@click.command()
@click.pass_obj
def stop(times_model: Times) -> None:
    """Signals the end of the clock"""
    times_model.register_out()


@click.command()
@click.option(
    "--date-from",
    "-df",
    "date_from",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=None,
)
@click.option(
    "--date-to",
    "-dt",
    "date_to",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    default=None,
)
@click.option(
    "--today",
    "-t",
    "today",
    is_flag=True,
    help="Shows today registers",
)
@click.option(
    "--raw",
    "-r",
    "raw",
    is_flag=True,
    help="Shows database registers with no modification",
)
@click.pass_obj
def show(
    times_model: Times,
    date_from: datetime,
    date_to: datetime,
    today: bool = False,
    raw: bool = False,
) -> None:
    """Shows current registers"""

    filters = {
        "date_from": date_from,
        "date_to": date_to,
    }

    if today:
        filters = {
            "date_from": datetime.today().strftime("%Y-%m-%d"),
            "date_to": datetime.today().strftime("%Y-%m-%d"),
        }

    if raw:
        registers = times_model.query_all(filters)

        if not registers:
            click.secho("No registers available", fg="yellow")
            return

        click.echo(
            tabulate(
                times_model.query_all(filters),
                headers=[header_style("Operation"), header_style("Date")],
                tablefmt="fancy_grid",
            )
        )
        return

    days = times_model.query_days(filters)

    if not days:
        click.secho("No registers available", fg="yellow")
        return

    click.secho(
        tabulate(
            [day.tuple() for day in days],
            headers=[
                header_style("Day"),
                header_style("From"),
                header_style("To"),
                header_style("Hours"),
            ],
            tablefmt="fancy_grid",
        ),
        fg="green",
    )


@click.command()
@click.pass_obj
def drop(times_model: Times) -> None:
    """Destroys all registers"""
    times_model.clear_db()


@click.group(commands=[start, stop, show, drop])
@click.version_option(None, "--version", package_name="timekeeper")
@click.option(
    "--database",
    "-db",
    "database",
    default="timekeeper.db",
    type=str,
    help="Database filename",
)
@click.pass_context
def cli(context=None, database: str = None) -> None:
    """CLI Runner group"""

    context.obj = Times(database)


if __name__ == "__main__":
    cli()
