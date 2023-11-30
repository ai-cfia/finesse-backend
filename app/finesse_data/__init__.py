import logging

import requests
from fuzzywuzzy import process


class FinesseDataException(Exception):
    """Custom exception for finesse-data operations."""


class FinesseDataFetchException(FinesseDataException):
    """Custom exception for errors in fetching data from finesse-data."""


class FinesseDataFilenameFetchException(FinesseDataException):
    """Custom exception for errors in fetching filenames from finesse-data."""


class EmptyQueryError(FinesseDataException):
    """Raised when the search query is empty."""


def find_best_match(search_string, candidates, match_threshold):
    best_match_result = process.extractOne(search_string, candidates)
    if not best_match_result or best_match_result[1] < match_threshold:
        logging.info(f"No close match found for search string: {search_string}")
        return None
    return best_match_result[0]


def fetch(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def fetch_data(finesse_data_url, query, match_threshold):
    if not query:
        logging.error("Empty search query received")
        raise EmptyQueryError("Search query cannot be empty")

    try:
        files = fetch(finesse_data_url)
        file_map = {file["name"]: file for file in files}
        if best_match := find_best_match(query, file_map.keys(), match_threshold):
            matching_file = file_map[best_match]
            results_response = requests.get(matching_file["download_url"])
            results_response.raise_for_status()
            return results_response.json()
    except requests.RequestException as e:
        logging.error(f"finesse-data fetch failed: {e}", exc_info=True)
        raise FinesseDataFetchException(f"Data fetch failed: {e}") from e
    except Exception as e:
        logging.error(str(e), exc_info=True)
        raise FinesseDataException(str(e)) from e


def fetch_filenames(finesse_data_url):
    try:
        files = fetch(finesse_data_url)
        filenames = [
            file["name"].replace(".json", "")
            for file in files
            if file["type"] == "file" and file["name"].endswith(".json")
        ]
        return filenames
    except requests.RequestException as e:
        logging.error(f"finesse-data filenames fetch failed: {e}", exc_info=True)
        raise FinesseDataFilenameFetchException(f"Filenames fetch failed: {e}") from e
    except Exception as e:
        logging.error(str(e), exc_info=True)
        raise FinesseDataException(str(e)) from e
