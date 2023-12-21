from flask import Blueprint

monitor_blueprint = Blueprint("monitor", __name__)


@monitor_blueprint.route("", methods=["GET"])
def health():
    return "ok", 200
