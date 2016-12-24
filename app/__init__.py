
from flask import Flask
from config import config


def create_app(environment):
    # configure flask webapp + assign static folder
    app = Flask(__name__, static_url_path="", static_folder="../resources/static")
    app.config.from_object(config[environment])

    # import modules
    from app.mod_home import home_blueprint
    from app.mod_favorites import favorites_blueprint
    from app.mod_history import history_blueprint
    from app.mod_api_handler import api_handler__blueprint

    # register blueprint
    app.register_blueprint(home_blueprint)
    app.register_blueprint(favorites_blueprint)
    app.register_blueprint(history_blueprint)
    app.register_blueprint(api_handler__blueprint, url_prefix="/api")

    return app
