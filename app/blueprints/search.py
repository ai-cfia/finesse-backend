import logging

from flask import Blueprint, current_app, jsonify, request
from index_search import AzureIndexSearchQueryError, search

from app.ailab_db import DBError, ailab_db_search
from app.blueprints.common import create_error_response
from app.finesse_data import FinesseDataFetchException, fetch_data
from app.utils import sanitize

search_blueprint = Blueprint("finesse", __name__)


class EmptyQueryError(Exception):
    """Raised when the search query is empty."""


@search_blueprint.errorhandler(AzureIndexSearchQueryError)
def handle_azure_error(error):
    message = current_app.config["ERROR_AZURE_FAILED"]
    return create_error_response(error, message, 500)


@search_blueprint.errorhandler(FinesseDataFetchException)
def handle_finesse_data_error(error):
    message = current_app.config["ERROR_FINESSE_DATA_FAILED"]
    return create_error_response(error, message, 500)


@search_blueprint.errorhandler(DBError)
def handle_db_error(error):
    message = current_app.config["ERROR_AILAB_FAILED"]
    return create_error_response(error, message, 500)


@search_blueprint.errorhandler(EmptyQueryError)
def handle_empty_query_error(error):
    message = current_app.config["ERROR_EMPTY_QUERY"]
    return create_error_response(error, message, 400)


@search_blueprint.errorhandler(Exception)
def handle_unexpected_error(error):
    message = current_app.config["ERROR_UNEXPECTED"]
    return create_error_response(error, message, 500)


def get_non_empty_query():
    query = request.json.get("query")
    if not query:
        message = current_app.config["ERROR_EMPTY_QUERY"]
        logging.error(message, exc_info=True)
        raise EmptyQueryError(message)
    return sanitize(query, current_app.config["SANITIZE_PATTERN"])


@search_blueprint.route("/azure", methods=["POST"])
def search_azure():
    query = get_non_empty_query()
    results = search(query, current_app.config["AZURE_CONFIG"])
    return jsonify(results)


@search_blueprint.route("/static", methods=["POST"])
def search_static():
    finesse_data_url = current_app.config["FINESSE_DATA_URL"]
    query = get_non_empty_query()
    match_threshold = current_app.config["FUZZY_MATCH_THRESHOLD"]
    data = fetch_data(finesse_data_url, query, match_threshold)
    return jsonify(data)


@search_blueprint.route("/ailab", methods=["POST"])
def search_ailab_db():
    query = get_non_empty_query()
    results = ailab_db_search(query)
    return jsonify(results)
