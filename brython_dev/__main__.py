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
@click.option("--app", prompt=True, help="Proyect app", default="app.py")
@click.option("--template", prompt=True, help="Proyect template", default="app.html")
def init(name, app, template):
    """Creates a basic brython.yml file in the current directory."""

    if Path(name.lower().replace("-", "_")).is_dir():
        app = f"{name.lower().replace('-', '_')}\{app}"
        template = f"{name.lower().replace('-', '_')}\{template}"
    
    
    with Path("brython.yml") as file:
        file.write_text(f"name: {name}\napp: {app}\ntemplate: {template}")


if __name__ == "__main__":  # pragma: no cover
    cli(prog_name="bython-dev")
