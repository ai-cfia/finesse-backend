from functools import wraps

from flask import current_app, jsonify, request
from flask_restx import Namespace, Resource, fields
from index_search import AzureIndexSearchQueryError, search

from app.ailab_db import DBError, ailab_db_search
from app.finesse_data import FinesseDataFetchException, fetch_data
from app.utils import sanitize

search_namespace = Namespace("search",description="Search operations")

search_model = search_namespace.model('SearchInput', {
    'query': fields.String,
})

def require_non_empty_query(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        query = request.json.get("query")
        if not query:
            return jsonify({"message": current_app.config["ERROR_EMPTY_QUERY"]}), 400
        return f(*args, **kwargs)

    return decorated_function


@search_namespace.route("/azure")
class Azure(Resource):
    @require_non_empty_query
    @search_namespace.expect(search_model)
    def post(self):
        query = request.json["query"]
        query = sanitize(query, current_app.config["SANITIZE_PATTERN"])
        try:
            results = search(query, current_app.config["AZURE_CONFIG"])
            return jsonify(results)
        except AzureIndexSearchQueryError:
            return jsonify({"error": current_app.config["ERROR_AZURE_FAILED"]}), 500
        except Exception:
            return jsonify({"error": current_app.config["ERROR_UNEXPECTED"]}), 500


@search_namespace.route("/static")
class Static(Resource):
    @require_non_empty_query
    @search_namespace.expect(search_model)
    def post(self):
        finesse_data_url = current_app.config["FINESSE_DATA_URL"]
        query = request.json["query"]
        query = sanitize(query, current_app.config["SANITIZE_PATTERN"])
        match_threshold = current_app.config["FUZZY_MATCH_THRESHOLD"]
        try:
            data = fetch_data(finesse_data_url, query, match_threshold)
            return jsonify(data)
        except FinesseDataFetchException:
            return jsonify({"error": current_app.config["ERROR_FINESSE_DATA_FAILED"]}), 500
        except Exception:
            return jsonify({"error": current_app.config["ERROR_UNEXPECTED"]}), 500


@search_namespace.route("/ailab")
class AilabDB(Resource):
    @require_non_empty_query
    @search_namespace.expect(search_model)
    def post(self):
        query = request.json["query"]
        query = sanitize(query, current_app.config["SANITIZE_PATTERN"])
        try:
            results = ailab_db_search(query)
            return jsonify(results)
        except DBError:
            return jsonify({"error": current_app.config["ERROR_AILAB_FAILED"]}), 500
        except Exception:
            return jsonify({"error": current_app.config["ERROR_UNEXPECTED"]}), 500
