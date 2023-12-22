from dataclasses import asdict

from flask import Blueprint, jsonify

from app.api.common.api_version import ApiVersion

VERSION = ApiVersion(full="2", release_date="2024-01", deprecated=False)
version_blueprint = Blueprint("version", __name__)


@version_blueprint.route("", methods=["GET"])
def version():
    return jsonify({"version": asdict(VERSION)})
