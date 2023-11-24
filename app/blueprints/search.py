from functools import wraps

from flask import Blueprint, current_app, jsonify, request
from index_search import search

from app.finesse_data import fetch_data

search_blueprint = Blueprint("finesse", __name__)


def require_non_empty_query(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        query = request.json.get("query")
        if not query:
            return jsonify({"message": "Search query cannot be empty"}), 400
        return f(*args, **kwargs)

    return decorated_function


@search_blueprint.route("/azure", methods=["POST"])
@require_non_empty_query
def search_azure():
    query = request.json["query"]
    try:
        results = search(query, current_app.config["AZURE_CONFIG"])
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@search_blueprint.route("/static", methods=["POST"])
@require_non_empty_query
def search_static():
    finesse_data_url = current_app.config["FINESSE_DATA_URL"]
    query = request.json["query"]
    try:
        data = fetch_data(finesse_data_url, query)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
