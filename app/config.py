import os
from dataclasses import dataclass

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
from index_search import AzureIndexSearchConfig

load_dotenv()

DEFAULT_DEBUG_MODE = "False"
DEFAULT_ERROR_EMPTY_QUERY = "Search query cannot be empty"
DEFAULT_ERROR_AZURE_FAILED = "Azure index search failed."
DEFAULT_ERROR_FINESSE_DATA_FAILED = "finesse-data static search failed"
DEFAULT_ERROR_UNEXPECTED = "Unexpected error."
DEFAULT_FUZZY_MATCH_THRESHOLD = 90
DEFAULT_ERROR_AILAB_FAILED = "Ailab-db search failed."
DEFAULT_ERROR_UNEXPECTED = "Unexpected error."
DEFAULT_SANITIZE_PATTERN = (
    "[^\w \d\"#\$%&'\(\)\*\+,-\.\/:;?@\^_`{\|}~]+|\%\w+|;|/|\(|\)"
)


@dataclass
class Config:
    AZURE_CONFIG = AzureIndexSearchConfig(
        endpoint=os.getenv("FINESSE_BACKEND_AZURE_SEARCH_ENDPOINT"),
        api_key=os.getenv("FINESSE_BACKEND_AZURE_SEARCH_API_KEY"),
        index_name=os.getenv("FINESSE_BACKEND_AZURE_SEARCH_INDEX_NAME"),
        client=SearchClient(
            os.getenv("FINESSE_BACKEND_AZURE_SEARCH_ENDPOINT"),
            os.getenv("FINESSE_BACKEND_AZURE_SEARCH_INDEX_NAME"),
            AzureKeyCredential(os.getenv("FINESSE_BACKEND_AZURE_SEARCH_API_KEY")),
        ),
    )
    FINESSE_DATA_URL = os.getenv("FINESSE_BACKEND_STATIC_FILE_URL")
    DEBUG = (
        os.getenv("FINESSE_BACKEND_DEBUG_MODE", DEFAULT_DEBUG_MODE).lower() == "true"
    )
    ERROR_EMPTY_QUERY = os.getenv(
        "FINESSE_BACKEND_ERROR_EMPTY_QUERY", DEFAULT_ERROR_EMPTY_QUERY
    )
    ERROR_AZURE_FAILED = os.getenv(
        "FINESSE_BACKEND_ERROR_AZURE_FAILED", DEFAULT_ERROR_AZURE_FAILED
    )
    ERROR_FINESSE_DATA_FAILED = os.getenv(
        "FINESSE_BACKEND_ERROR_FINESSE_DATA_FAILED", DEFAULT_ERROR_FINESSE_DATA_FAILED
    )
    ERROR_AILAB_FAILED = os.getenv(
        "FINESSE_BACKEND_ERROR_AILAB_FAILED", DEFAULT_ERROR_AILAB_FAILED
    )
    ERROR_UNEXPECTED = os.getenv(
        "FINESSE_BACKEND_ERROR_UNEXPECTED", DEFAULT_ERROR_UNEXPECTED
    )
    FUZZY_MATCH_THRESHOLD = int(
        os.getenv(
            "FINESSE_BACKEND_FUZZY_MATCH_THRESHOLD", DEFAULT_FUZZY_MATCH_THRESHOLD
        )
    )
    SANITIZE_PATTERN = os.getenv(
        "FINESSE_BACKEND_SANITIZE_PATTERN", DEFAULT_SANITIZE_PATTERN
    )
