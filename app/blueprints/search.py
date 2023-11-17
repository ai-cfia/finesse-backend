from flask import Blueprint, current_app, jsonify, request

from app.azure_search import azure_search_documents

search = Blueprint("finesse", __name__)


@search.route("", methods=["POST"])
def search_documents():
    query = request.json["query"]
    results = azure_search_documents(query, current_app.config["AZURE_CONFIG"])
    return jsonify(results)
