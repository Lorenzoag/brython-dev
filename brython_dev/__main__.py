from pathlib import Path

import click
import yaml
from flask import Flask, render_template
from flask.cli import FlaskGroup

from brython_dev import __version__, create_app

PYTHON_TEMPLATE = """from browser import document, html

document['app'] <= html.SPAN('Hello Brython!')
"""
HTML_TEMPLATE = """<div id="app"></div>"""

MAIN_TEMPLATE = """
import argparse

def install(args):
    print(args)

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

install = subparser.add_parser('install', help='Install {name} in an empty directory')
install.set_defaults(func=install)

"""

PYTHON_TEMPLATE = """from browser import document, html

document['app'] <= html.SPAN('Hello Brython!')
"""
HTML_TEMPLATE = """<div id="app"></div>"""


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

    safe_name = Path(name.lower().replace("-", "_"))
    root = safe_name if safe_name.is_dir() else Path.cwd()

    with Path("brython.yml") as file:
        file.write_text(f"name: {name}\napp: {app}\ntemplate: {template}")
    with Path(root / app) as file:
        file.write_text(PYTHON_TEMPLATE)
    with Path(root / template) as file:
        file.write_text(HTML_TEMPLATE)


@cli.command()
def build():
    """Build the proyect."""

    safe_load = yaml.safe_load(Path("brython.yml").read_text())
    safe_name = Path(safe_load["name"].lower().replace("-", "_"))
    proyect = safe_name if safe_name.is_dir() else Path.cwd()

    with Path(proyect / "__main__.py") as file:
        file.write_text(MAIN_TEMPLATE)

    print(render_template("index.html"))


if __name__ == "__main__":  # pragma: no cover
    cli(prog_name="bython-dev")
