import click
from flask import Flask
from flask.cli import FlaskGroup

from brython_dev import __version__, create_app


@click.group(cls=FlaskGroup, create_app=create_app, add_version_option=False)
@click.version_option(version=__version__)
def cli():
    """Management script for brython developers."""


cli(prog_name="bython-dev")
