from flask import Blueprint

from .blueprints.monitor import monitor_blueprint
from .blueprints.search import search_blueprint

VERSION = "1"


def get_blueprint():
    bp = Blueprint(VERSION, __name__)
    bp.register_blueprint(monitor_blueprint, url_prefix="/health", strict_slashes=False)
    bp.register_blueprint(search_blueprint, url_prefix="/search", strict_slashes=False)
    return bp
