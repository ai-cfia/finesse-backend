from datetime import datetime
from app.azure_search import search_documents 
from flask import Blueprint, current_app, jsonify, request

blueprint = Blueprint("main", __name__)

@blueprint.before_request
def log_request_info():
    current_app.logger.debug("Headers: %s", request.headers)
    current_app.logger.debug("Body: %s", request.get_data())


@blueprint.route("/health", methods=["GET"])
def health():
    return "ok", 200


@blueprint.route("/")
def read_root():
    current_time = datetime.now()
    unix_timestamp = int(current_time.timestamp())
    return {"current_time": unix_timestamp}


@blueprint.route("/search", methods=["GET"])
def search():
    query = request.args.get('query', '')
    results = search_documents(query, current_app.config["AZURE_CONFIG"])  
    return jsonify(results)
