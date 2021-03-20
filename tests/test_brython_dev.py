import pkg_resources
import pytest

from brython_dev import __version__, create_app


def test_version():
    assert __version__ == pkg_resources.get_distribution("brython-dev").version


@pytest.mark.parametrize(
    ("path", "status"),
    (
        ("/brython.js", 200),
        ("/brython_stdlib.js", 200),
        ("/Lib/site-packages/easy_install.py", 200),
        ("/Lib/site-packages/brython.py", 404),
        ("/Lib/site-packages/brython/__init__.py", 200),
    ),
)
def test_routes(client, path, status):
    assert client.get(path).status_code == status
    # assert client.get("/brython_stdlib.js").status_code == 200

    # assert client.get("/Lib/site-packages/easy_install.py").status_code == 200
    # assert client.get("/Lib/site-packages/brython.py").status_code == 404
    # assert client.get("/Lib/site-packages/brython/__init__.py").status_code == 200


def test_not_config_file():
    # with pytest.raises(FileExistsError):
    create_app({"TESTING": True, "SECRET_KEY": "dev", "CONFIG_FILE": "incorrect.yml"})
