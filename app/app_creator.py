from flask import Flask

from .config import Config


def create_app(config: Config):
    app = Flask(__name__)
    app.config.from_object(config)

    from .blueprints.monitor import monitor
    from .blueprints.search import search

    app.register_blueprint(monitor, url_prefix="/health", strict_slashes=False)
    app.register_blueprint(search, url_prefix="/search", strict_slashes=False)

    return app
