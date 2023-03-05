"""CLI Interface module"""

import click


@click.command()
def start():
    """Signals the begining of the clock"""
    click.echo("Started")


@click.command()
def stop():
    """Signals the end of the clock"""
    click.echo("Stopped")


@click.command()
def show():
    """Shows current registers"""
    click.echo("Show")


@click.group(commands=[start, stop, show])
def cli():
    """CLI Runner group"""
    pass


if __name__ == "__main__":
    cli()
