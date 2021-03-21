from pathlib import Path

from brython_dev import __version__
from brython_dev.__main__ import cli


def test_factory(runner):
    assert runner.invoke(cli, ["--version"]).output == f"cli, version {__version__}\n"


def test_init(runner):
    runner.invoke(cli, ["init", "--name", "test"])

    with Path("brython.yml") as p:
        assert p.exists()
        p.unlink()
        assert not p.exists()
