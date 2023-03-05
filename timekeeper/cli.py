"""CLI Interface module"""

import click

from timekeeper.model import Times


@click.command()
@click.pass_obj
def start(times_model: Times):
    """Signals the begining of the clock"""
    times_model.register_in()


@click.command()
@click.pass_obj
def stop(times_model: Times):
    """Signals the end of the clock"""
    times_model.register_out()


@click.command()
@click.pass_obj
def show(times_model: Times):
    """Shows current registers"""
    registers = times_model.query_times()
    for items in registers:
        print(items)


@click.command()
@click.pass_obj
def drop(times_model: Times):
    """Destroys all registers"""
    times_model.clear_db()


@click.group(commands=[start, stop, show, drop])
@click.pass_context
def cli(context=None):
    """CLI Runner group"""

    context.obj = Times("timekeeper.db")


if __name__ == "__main__":
    cli()
