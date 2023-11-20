from flask import Blueprint, current_app, jsonify, request
from index_search import search as azure_index_search

search = Blueprint("finesse", __name__)


@search.route("", methods=["POST"])
def search_documents():
    query = request.json["query"]
    results = azure_index_search(query, current_app.config["AZURE_CONFIG"])
    return jsonify(results)
