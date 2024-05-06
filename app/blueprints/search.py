import logging

from ailab_llamaindex_search import search as llamaindex_search
from flask import Blueprint, current_app, jsonify, request
from index_search import AzureIndexSearchError, search

from app.blueprints.common import create_error_response
from app.config import Config
from app.finesse_data import FinesseDataFetchException, fetch_data
from app.utils import sanitize

search_blueprint = Blueprint("finesse", __name__)


class EmptyQueryError(Exception):
    """Raised when the search query is empty."""


@search_blueprint.errorhandler(AzureIndexSearchError)
def handle_azure_error(error):
    logging.exception(error)
    message = current_app.config["ERROR_AZURE_FAILED"]
    return create_error_response(error, message, 500)


@search_blueprint.errorhandler(FinesseDataFetchException)
def handle_finesse_data_error(error):
    logging.exception(error)
    message = current_app.config["ERROR_FINESSE_DATA_FAILED"]
    return create_error_response(error, message, 500)


@search_blueprint.errorhandler(EmptyQueryError)
def handle_empty_query_error(error):
    logging.exception(error)
    message = current_app.config["ERROR_EMPTY_QUERY"]
    return create_error_response(error, message, 400)


@search_blueprint.errorhandler(Exception)
def handle_unexpected_error(error):
    logging.exception(error)
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
    config: Config = current_app.config
    skip = request.args.get("skip", config["DEFAULT_AZURE_SEARCH_SKIP"], int)
    top = request.args.get("top", config["DEFAULT_AZURE_SEARCH_TOP"], int)
    query = get_non_empty_query()
    search_params = {**config["AZURE_SEARCH_PARAMS"], "skip": skip, "top": top}
    client = config["AZURE_SEARCH_CLIENT"]
    transform_map = config["AZURE_SEARCH_TRANSFORM_MAP"]
    results = search(query, client, search_params, transform_map)
    return jsonify(results)


@search_blueprint.route("/static", methods=["POST"])
def search_static():
    finesse_data_url = current_app.config["FINESSE_DATA_URL"]
    query = get_non_empty_query()
    match_threshold = current_app.config["FUZZY_MATCH_THRESHOLD"]
    data = fetch_data(finesse_data_url, query, match_threshold)
    return jsonify(data)


@search_blueprint.route("/llamaindex", methods=["POST"])
def search_ailab_llamaindex():
    config: Config = current_app.config
    top = request.args.get("top", config["DEFAULT_AILAB_LLAMAINDEX_SEARCH_TOP"], int)
    query = get_non_empty_query()
    index = config["AILAB_LLAMAINDEX_SEARCH_INDEX"]
    trans_paths = config["AILAB_LLAMAINDEX_SEARCH_TRANS_PATHS"]
    results = llamaindex_search(query, index, top, trans_paths)
    return jsonify(results)
