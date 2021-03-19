import pkg_resources
import pytest

from brython_dev import __version__, create_app


def test_version():
    assert __version__ == pkg_resources.get_distribution("brython-dev").version


def test_routes(client):
    assert client.get("/brython.js").status_code == 200
    assert client.get("/brython_stdlib.js").status_code == 200

    assert client.get("/Lib/site-packages/easy_install.py").status_code == 200
    assert client.get("/Lib/site-packages/brython.py").status_code == 404
    assert client.get("/Lib/site-packages/brython/__init__.py").status_code == 200


def test_raise_config():
    with pytest.raises(FileExistsError):
        create_app(
            {"TESTING": True, "SECRET_KEY": "dev", "CONFIG_FILE": "incorrect.yml"}
        )
