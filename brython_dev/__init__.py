import sysconfig
from pathlib import Path

import pkg_resources
import yaml
from flask import Flask, escape, render_template, send_from_directory

try:
    __version__ = pkg_resources.get_distribution("brython-dev").version
except pkg_resources.DistributionNotFound:  # pragma: no cover
    __version__ = "unknown"


def create_app(config: dict = {}) -> Flask:
    config_file = Path(config.get("CONFIG_FILE", "brython.yml")).resolve()

    config_yaml = (
        {k.upper(): v for k, v in yaml.safe_load(config_file.read_text()).items()}
        if config_file.exists()
        else {"NAME": "Unnamed"}
    )

    proyect = Path.cwd()
    if Path(config_yaml["NAME"].lower().replace("-", "_")).is_dir():
        proyect = Path(config_yaml["NAME"].lower().replace("-", "_"))

    app = Flask(
        __name__,
        static_folder=str(proyect.resolve()),
        static_url_path=config_yaml.get("STATIC_URL", "/"),
    )

    app.config.from_mapping(config_yaml)
    app.config.from_mapping(config)

    @app.template_filter()
    def pretty_dict(_dict):
        return f"{{{', '.join(f'{k}: {v}' for k, v in _dict.items())}}}"

    @app.template_filter()
    def read_text(filename):
        return (
            Path(proyect / filename).read_text()
            if Path(proyect / filename).exists()
            else ""
        )

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/brython.js")
    def brythonjs():
        return send_from_directory(
            sysconfig.get_path("purelib"), "brython/data/brython.js"
        )

    @app.route("/brython_stdlib.js")
    def brythonstdlibjs():
        return send_from_directory(
            sysconfig.get_path("purelib"), "brython/data/brython_stdlib.js"
        )

    @app.route("/Lib/site-packages/<path:filename>")
    def site_packages(filename: str):
        return send_from_directory(sysconfig.get_path("purelib"), filename)

    return app
