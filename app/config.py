import json
import os
from typing import TypedDict

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv

load_dotenv()

# Constants
DEFAULT_DEBUG_MODE = "False"
DEFAULT_ERROR_EMPTY_QUERY = "Search query cannot be empty"
DEFAULT_ERROR_AZURE_FAILED = "Azure index search failed."
DEFAULT_ERROR_FINESSE_DATA_FAILED = "finesse-data static search failed"
DEFAULT_ERROR_UNEXPECTED = "Unexpected error."
DEFAULT_FUZZY_MATCH_THRESHOLD = 90
DEFAULT_ERROR_AILAB_FAILED = "Ailab-db search failed."
DEFAULT_SANITIZE_PATTERN = (
    "[^\w \d\"#\$%&'\(\)\*\+,-\.\/:;?@\^_`{\|}~]+|\%\w+|;|/|\(|\)"
)
DEFAULT_HIGHLIGHT_FIELDS = "content"
DEFAULT_HIGHLIGHT_TAG = "strong"
DEFAULT_AZURE_SEARCH_SKIP = 0
DEFAULT_AZURE_SEARCH_TOP = 10
DEFAULT_AZURE_SEARCH_TRANSFORM_MAP_JSON = {
    "id": "/id",
    "title": "/title",
    "score": "/@search.score",
    "url": "/url",
    "content": "/@search.highlights/content/0",
    "last_updated": "/last_updated",
}
DEFAULT_AZURE_SEARCH_PARAMS = {
    "highlight_fields": "content",
    "highlight_pre_tag": "<strong>",
    "highlight_post_tag": "</strong>",
}


class Config(TypedDict):
    AZURE_SEARCH_SKIP: int
    AZURE_SEARCH_TOP: int
    AZURE_SEARCH_CLIENT: SearchClient
    AZURE_SEARCH_PARAMS: dict
    AZURE_SEARCH_TRANSFORM_MAP: dict
    FINESSE_DATA_URL: str
    DEBUG: bool
    ERROR_EMPTY_QUERY: str
    ERROR_AZURE_FAILED: str
    ERROR_FINESSE_DATA_FAILED: str
    ERROR_AILAB_FAILED: str
    ERROR_UNEXPECTED: str
    FUZZY_MATCH_THRESHOLD: int
    SANITIZE_PATTERN: str


def create_config() -> Config:
    azure_search_client = SearchClient(
        endpoint=os.getenv("FINESSE_BACKEND_AZURE_SEARCH_ENDPOINT", ""),
        index_name=os.getenv("FINESSE_BACKEND_AZURE_SEARCH_INDEX_NAME", ""),
        credential=AzureKeyCredential(
            os.getenv("FINESSE_BACKEND_AZURE_SEARCH_API_KEY", "")
        ),
    )
    azure_search_transform_map = (
        json.loads(os.getenv("FINESSE_BACKEND_AZURE_SEARCH_TRANSFORM_MAP", "{}"))
        or DEFAULT_AZURE_SEARCH_TRANSFORM_MAP_JSON
    )
    azure_search_params = (
        json.loads(os.getenv("FINESSE_BACKEND_AZURE_SEARCH_PARAMS", "{}"))
        or DEFAULT_AZURE_SEARCH_PARAMS
    )

    return {
        "AZURE_SEARCH_SKIP": DEFAULT_AZURE_SEARCH_SKIP,
        "AZURE_SEARCH_TOP": DEFAULT_AZURE_SEARCH_TOP,
        "AZURE_SEARCH_CLIENT": azure_search_client,
        "AZURE_SEARCH_PARAMS": azure_search_params,
        "AZURE_SEARCH_TRANSFORM_MAP": azure_search_transform_map,
        "FINESSE_DATA_URL": os.getenv("FINESSE_BACKEND_STATIC_FILE_URL"),
        "DEBUG": os.getenv("FINESSE_BACKEND_DEBUG_MODE", DEFAULT_DEBUG_MODE).lower()
        == "true",
        "ERROR_EMPTY_QUERY": os.getenv(
            "FINESSE_BACKEND_ERROR_EMPTY_QUERY", DEFAULT_ERROR_EMPTY_QUERY
        ),
        "ERROR_AZURE_FAILED": os.getenv(
            "FINESSE_BACKEND_ERROR_AZURE_FAILED", DEFAULT_ERROR_AZURE_FAILED
        ),
        "ERROR_FINESSE_DATA_FAILED": os.getenv(
            "FINESSE_BACKEND_ERROR_FINESSE_DATA_FAILED",
            DEFAULT_ERROR_FINESSE_DATA_FAILED,
        ),
        "ERROR_AILAB_FAILED": os.getenv(
            "FINESSE_BACKEND_ERROR_AILAB_FAILED", DEFAULT_ERROR_AILAB_FAILED
        ),
        "ERROR_UNEXPECTED": os.getenv(
            "FINESSE_BACKEND_ERROR_UNEXPECTED", DEFAULT_ERROR_UNEXPECTED
        ),
        "FUZZY_MATCH_THRESHOLD": int(
            os.getenv(
                "FINESSE_BACKEND_FUZZY_MATCH_THRESHOLD",
                str(DEFAULT_FUZZY_MATCH_THRESHOLD),
            )
        ),
        "SANITIZE_PATTERN": os.getenv(
            "FINESSE_BACKEND_SANITIZE_PATTERN", DEFAULT_SANITIZE_PATTERN
        ),
    }
