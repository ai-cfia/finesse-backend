from flask import Flask
from flask_cors import CORS

from .config import Config


def create_app(config: Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)

    from .api import v1, v2

    app.register_blueprint(
        v1.get_blueprint(), url_prefix=f"/api/v{v1.VERSION}", strict_slashes=False
    )
    app.register_blueprint(
        v2.get_blueprint(), url_prefix=f"/api/v{v2.VERSION}", strict_slashes=False
    )

    return app
