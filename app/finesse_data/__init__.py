import logging

import requests


class FinesseDataFetchException(Exception):
    """Custom exception for errors in fetching data from finesse-data."""


class EmptyQueryError(Exception):
    """Raised when the search query is empty."""


def fetch_data(finesse_data_url, query):
    if not query:
        logging.error("Empty search query received")
        raise EmptyQueryError("Search query cannot be empty")
    try:
        response = requests.get(finesse_data_url)
        response.raise_for_status()
        files = response.json()
        normalized_term = query.lower()
        matching_file = next(
            (file for file in files if normalized_term in file["name"].lower()), None
        )
        if not matching_file:
            logging.info("No matching file found for query: %s", query)
            return None
        results_response = requests.get(matching_file["download_url"])
        results_response.raise_for_status()
        return results_response.json()
    except requests.RequestException as e:
        raise FinesseDataFetchException(f"API request failed: {e}") from e
