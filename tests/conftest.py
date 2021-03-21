# import atexit
# import tempfile
# from contextlib import contextmanager
# from pathlib import Path

import pytest

from brython_dev import create_app


@pytest.fixture
def app():
    yield create_app(
        {"TESTING": True, "SECRET_KEY": "dev", "CONFIG_FILE": "tests/brython.yml"}
    )


@pytest.fixture
def client(app):
    yield app.test_client()


@pytest.fixture
def runner(app):
    yield app.test_cli_runner()


# @pytest.fixture
# def log(app):
# return app.logger


# class AuthActions:
# _csrf_token = None
# _client = None

# default_email =
# default_password =

# def __init__(self, client):
# self._client = client

# @property
# def csrf_token(self):
# if self._csrf_token is None:
# self._csrf_token = self._
# return self._csrf_token

# def register(self, email=None, password=None):
# return self._client.post(
# "/auth/register",
# json={
# "email": email or self.default_email,
# "password": password or self.default_password,
# "csrf_token": self.csrf_token,
# },
# )

# def login(self, email=None, password=None):
# return self._client.post(
# "/auth/login",
# json={
# "email": email or self.default_email,
# "password": password or self.default_password,
# "csrf_token": self.csrf_token,
# },
# )

# def logout(self):
# return self._client.get("/auth/logout")

# @pytest.fixture
# def csrf_token(client):
# with client:
# return client.get("/auth/login", json={}).json["response"]["csrf_token"]


# @pytest.fixture
# def auth(client, csrf_token):
