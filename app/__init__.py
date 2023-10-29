from flask import Flask
from config import config

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .main_blueprint import main
    app.register_blueprint(main, url_prefix="/")
    return app
