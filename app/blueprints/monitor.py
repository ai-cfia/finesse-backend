from flask import Blueprint

monitor = Blueprint("monitor", __name__)


@monitor.route("", methods=["GET"])
def health():
    return "ok", 200
