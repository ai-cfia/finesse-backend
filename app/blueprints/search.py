from flask import Blueprint, current_app, jsonify, request
from index_search import search as azure_index_search

from app.finesse_data import fetch_data as static_data_search

search = Blueprint("finesse", __name__)


@search.route("/azure", methods=["POST"])
def search_azure():
    query = request.json["query"]
    results = azure_index_search(query, current_app.config["AZURE_CONFIG"])
    return jsonify(results)


@search.route("/static", methods=["POST"])
def search_static():
    finesse_data_url = current_app.config["FINESSE_DATA_URL"]
    query = request.json.get("query")
    data = static_data_search(finesse_data_url, query)
    return jsonify(data)
