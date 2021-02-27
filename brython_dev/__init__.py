import pkg_resources, sysconfig
from flask import Flask, render_template, send_file, send_from_directory
import yaml
from pathlib import Path

try:
    __version__ = pkg_resources.get_distribution('brython-dev').version
except pkg_resources.DistributionNotFound:
    __version__ = 'unknown'
    

def create_app(config: dict = {}) -> Flask:
    app = Flask(__name__)
    
    config_file = Path("brython.yml").resolve()
    if config_file.exists():
        with open(config_file, "r") as fh:
            app.config.from_mapping(yaml.safe_load(fh.read()))
    
    app.config.from_mapping(config)
    
    @app.route('/')
    def index():
        return render_template('index.html')
                                # stylesheets=app.config.get('stylesheets', []))
                                # scripts=app.config.get('scripts', []),
                                # extensions=app.config.get('extensions', {}),
                                # options=app.config.get('options', {}),
        # )
    
    # @app.route("/<path:path>")
    # def catch_all(path: str):
        # send_file(path)
    
    

    # @app.route('/lib/site-packages/<path:path>')
    # def site_packages(path: str):
        # send_from_directory(sysconfig.get_path("purelib"), path)
    
    
    return app