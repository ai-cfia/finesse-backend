import traceback

from flask import current_app, jsonify


def create_error_response(error, message, status_code):
    """Create an error response based on debug mode"""
    if current_app.debug:
        payload = {
            "error": message,
            "details": str(error),
            "trace": traceback.format_exc(),
        }
        return jsonify(payload), status_code
    else:
        return jsonify({"error": message}), status_code
