from brython_dev import create_app


def test_config(app):
    assert app.testing
    assert app.secret_key == "dev"


def test_hello(client):
    response = client.get("/")
    assert response.status_code == 200
