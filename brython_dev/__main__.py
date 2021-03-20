from pathlib import Path

import click
from flask import Flask
from flask.cli import FlaskGroup

from brython_dev import __version__, create_app


@click.group(cls=FlaskGroup, create_app=create_app, add_version_option=False)
@click.version_option(version=__version__)
def cli():
    """Management script for brython developers."""


@cli.command()
@click.option("--name", prompt=True, help="Proyect name")
def init(name):  # , app, template):
    """Creates a basic brython.yml file in the current directory."""

    with Path("brython.yml") as file:
        file.write_text(f"name: {name}")


if __name__ == "__main__":  # pragma: no cover
    cli(prog_name="bython-dev")
