import sysconfig
from pathlib import Path

import pkg_resources
import yaml
from flask import Flask, render_template, send_file, send_from_directory, escape

try:
    __version__ = pkg_resources.get_distribution("brython-dev").version
except pkg_resources.DistributionNotFound:
    __version__ = "unknown"


def create_app(config: dict = {}) -> Flask:
    app = Flask(__name__)

    config_file = Path("brython.yml").resolve()
    if config_file.exists():
        with open(config_file, "r") as fh:
            parse = yaml.safe_load(fh.read())
            app.config["NAME"] = parse.get("name") or "Unnamed"
            app.config["STYLESHEETS"] = parse.get("stylesheets") or []
            app.config["EXTENSIONS"] = parse.get("extensions") or {}
            app.config["USE_BRYTHON"] = app.config["EXTENSIONS"].get("brython") or True
            app.config["USE_BRYTHON_STDLIB"] = (
                app.config["EXTENSIONS"].get("brython_stdlib") or False
            )
            app.config["SCRIPTS"] = parse.get("scripts") or {}
            brython_options = parse.get("brython_options") or {"debug": 1}
            app.config["BRYTHON_OPTIONS"] = (
                escape("{" + ", ".join(f"{k}: {v}" for k, v in brython_options.items()) + "}")
            )
            app.config["APP"] = parse.get("app") or 'app.py'
            template = parse.get("template") or 'app.html'
            if Path(template).exists():
                with open(template, "r") as ft:
                    template = ft.read()
            else:
                template = ""
            app.config["TEMPLATE"] = template

    app.config.from_mapping(config)

    @app.route("/")
    def index():
        return render_template(
            "index.html",
            name=app.config["NAME"],
            stylesheets=app.config["STYLESHEETS"],
            use_brython=app.config["USE_BRYTHON"],
            use_brython_stdlib=app.config["USE_BRYTHON_STDLIB"],
            scripts=app.config["SCRIPTS"],
            brython_options=app.config["BRYTHON_OPTIONS"],
            app=app.config["APP"],
            template=app.config["TEMPLATE"],
        )

    # @app.route("/<path:path>")
    # def catch_all(path: str):
    # send_file(path)

    # @app.route('/lib/site-packages/<path:path>')
    # def site_packages(path: str):
    # send_from_directory(sysconfig.get_path("purelib"), path)

    return app
