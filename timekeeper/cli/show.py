"""Show Interface module"""

from datetime import datetime
from functools import partial

import click
from tabulate import tabulate

from timekeeper.cli.session import CliSession
from timekeeper.model import Session
from timekeeper.remote import Hiper


def header_style(text: str) -> str:
    """Helper styling function"""
    partial_func = partial(click.style, fg="green", bold=True)
    return partial_func(text)


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
@click.option(
    "--inform",
    "-i",
    "inform_remote",
    is_flag=True,
    help="Registers the filtered days to a remote server",
)
@click.pass_obj
def show(
    session: CliSession,
    date_from: datetime,
    date_to: datetime,
    today: bool = False,
    raw: bool = False,
    inform_remote: bool = False,
) -> None:
    """Shows current registers"""

    filters = {}

    if date_from:
        filters["date_from"] = f"{date_from} 00:00:00"
    if date_to:
        filters["date_to"] = f"{date_to} 23:59:59"

    if today:
        filters = {
            "date_from": datetime.today().strftime("%Y-%m-%d 00:00:00"),
            "date_to": datetime.today().strftime("%Y-%m-%d 23:59:59"),
        }

    if raw:
        registers = session.times_model.query_all(filters)

        if not registers:
            click.secho("No registers available", fg="yellow")
            return

        click.echo(
            tabulate(
                session.times_model.query_all(filters=filters),
                headers=[header_style("Operation"), header_style("Date")],
                tablefmt="fancy_grid",
            )
        )
        return

    days = session.times_model.query_days(filters=filters)

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

    if inform_remote:
        click.echo("Communicating to remote...")

        remote = Hiper()

        if not session.session_model.get_cookies():
            session_cookies = remote.login(
                session.config.hiper["user"], session.config.hiper["user"]
            )
            if not session_cookies:
                click.Abort("Could not login to Hiper")

            session.session_model.set_cookies(session_cookies)

        for day in days:
            comm = remote.register_date(
                day,
                session.session_model.get_cookies(),
            )
            if comm:
                click.secho(f"{day.day_str()} informed correctly", fg="green")
            else:
                click.secho(f"{day.day_str()} could not be informed", fg="red")

        click.echo("Communication finished...")
