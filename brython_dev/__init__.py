import sysconfig
from pathlib import Path

import pkg_resources
import yaml
from flask import Flask, escape, render_template_string, send_from_directory

try:
    __version__ = pkg_resources.get_distribution("brython-dev").version
except pkg_resources.DistributionNotFound:  # pragma: no cover
    __version__ = "unknown"

    
INDEX_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>{{ config.get("NAME") or "Unnamed" }}</title>
    <meta charset="utf-8">
    {% for stylesheet in config.get("STYLESHEETS") or [] %}
    <link rel="stylesheet" href="{{ stylesheet }}">{% endfor %}
    {% if config.get("EXTENSIONS", {}).get("brython", True) %}
    <script type="text/javascript" src="/brython.js"></script>{% endif %}{% if config.get("EXTENSIONS", {}).get("brython_stdlib", False) %}
    <script type="text/javascript" src="/brython_stdlib.js"></script>{% endif %}{% for script in config.get("SCRIPTS") or [] %}
    <script type="text/javascript" src="{{ script }}"></script>{% endfor %}
</head>
<body onload="brython({{ config.get('BRYTHON_OPTIONS', {'debug': 1})|pretty_dict }})">
    <!--{{ config.get("TEMPLATE", "app.html")|read_text|safe }}-->
    <script id="load.py" type="text/python3">
    from browser import document, html
    document.select("body")[0] <= html.DIV(open("{{ config.get("TEMPLATE", "app.html") }}").read())
    </script>
    {% if config.get("CONSOLE", True) and config.get("EXTENSIONS", {}).get("brython_stdlib", False) %}
    <script id="console.py" type="text/python3">
    from interpreter import Interpreter
    import sys
    sys.stdout = sys.stderr = Interpreter()
    print("\\n")
    </script>
    {% endif %}
    <script id="app.py" type="text/python3" src="{{ config.get('APP', 'app.py') }}"></script>
</body>
</html>
"""

def create_app(config: dict = {}) -> Flask:
    config_file = Path(config.get("CONFIG_FILE", "brython.yml")).resolve()

    config_yaml = (
        {k.upper(): v for k, v in yaml.safe_load(config_file.read_text()).items()}
        if config_file.exists()
        else {"NAME": "Unnamed"}
    )

    proyect = Path.cwd()
    if Path(config_yaml["NAME"].lower().replace("-", "_")).is_dir():  # pragma: no cover
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
        return render_template_string(INDEX_TEMPLATE)

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
