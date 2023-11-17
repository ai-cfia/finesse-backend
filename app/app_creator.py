from flask import Flask

from .config import Config


def create_app(config: Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Register the main blueprint
    from .routes import blueprint as main_blueprint
    app.register_blueprint(main_blueprint)

    # Configure Membrane login.
    return app
