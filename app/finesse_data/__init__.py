import logging
import requests
from fuzzywuzzy import process

class FinesseDataFetchException(Exception):
    """Custom exception for errors in fetching data from finesse-data."""

class EmptyQueryError(Exception):
    """Raised when the search query is empty."""

def fetch_data(finesse_data_url, query, match_threshold):
    if not query:
        logging.error("Empty search query received")
        raise EmptyQueryError("Search query cannot be empty")

    try:
        response = requests.get(finesse_data_url)
        response.raise_for_status()
        files = response.json()
        file_map = {file["name"]: file for file in files}
        query = query.replace("\r\n", "").replace("\n", "")
        best_match_result = process.extractOne(query, file_map.keys())
        if not best_match_result or best_match_result[1] < match_threshold:
            logging.info(f"No close match found for query: {query}")
            return None
        best_match, _ = best_match_result
        matching_file = file_map[best_match]
        results_response = requests.get(matching_file["download_url"])
        results_response.raise_for_status()
        return results_response.json()
    except requests.RequestException as e:
        logging.error(f"finesse-data fetch failed: {e}", exc_info=True)
        raise FinesseDataFetchException(f"finesse-data fetch failed: {e}") from e
