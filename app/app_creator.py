from flask import Flask
from flask_cors import CORS


def create_app(config):
    app = Flask(__name__)
    CORS(app)
    app.config.update(config)

    from .blueprints.monitor import monitor_blueprint
    from .blueprints.search import search_blueprint

    app.register_blueprint(
        monitor_blueprint, url_prefix="/health", strict_slashes=False
    )
    app.register_blueprint(search_blueprint, url_prefix="/search", strict_slashes=False)

    return app
