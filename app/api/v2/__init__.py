from flask import Blueprint

from .blueprints.monitor import monitor_blueprint
from .blueprints.search import search_blueprint
from .blueprints.version import VERSION, version_blueprint


def get_blueprint():
    bp = Blueprint(VERSION.full, __name__)
    bp.register_blueprint(monitor_blueprint, url_prefix="/health")
    bp.register_blueprint(search_blueprint, url_prefix="/search")
    bp.register_blueprint(version_blueprint, url_prefix="/version")
    return bp
