from pathlib import Path

from brython_dev import __version__
from brython_dev.__main__ import cli


def remove_file_or_dir(file_or_dir):
    with Path(file_or_dir) as p:
        assert p.exists()
        if p.is_file():
            p.unlink()
        elif p.is_dir():
            for i in p.iterdir():
                remove_file_or_dir(i)
            p.rmdir()
        assert not p.exists()


def test_factory(runner):
    assert runner.invoke(cli, ["--version"]).output == f"cli, version {__version__}\n"


def test_init(runner):
    Path("test_dir").mkdir()

    runner.invoke(cli, ["init", "--name", "test-dir"])

    remove_file_or_dir("brython.yml")
    remove_file_or_dir("test_dir")


def test_build(runner):
    Path("test_dir").mkdir()
    runner.invoke(cli, ["init", "--name", "test-dir"])

    runner.invoke(cli, ["build"])

    remove_file_or_dir("brython.yml")
    remove_file_or_dir("test_dir")
