from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from .config import Config

def create_app(config: Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config)

    api = Api(path = "")
    api.init_app(app)

    from .namespaces.search import search_namespace
    from .namespaces.monitor import monitor_namespace

    api.add_namespace(search_namespace)
    api.add_namespace(monitor_namespace)
    return app
