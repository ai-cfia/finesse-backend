# Constants

# Flag to determine if debug mode is active, default is False
DEFAULT_DEBUG_MODE = "False"

# Default error message for empty search queries
DEFAULT_ERROR_EMPTY_QUERY = "Search query cannot be empty"

# Default error message when Azure search service fails
DEFAULT_ERROR_AZURE_FAILED = "Azure index search failed."

# Default error message for failures in finesse-data static search
DEFAULT_ERROR_FINESSE_DATA_FAILED = "finesse-data static search failed"

# Default error message for any unexpected errors encountered
DEFAULT_ERROR_UNEXPECTED = "Unexpected error."

# Threshold for fuzzy match scoring
DEFAULT_FUZZY_MATCH_THRESHOLD = 90

# Default error message when Ailab-db search fails
DEFAULT_ERROR_AILAB_FAILED = "Ailab-db search failed."

# Regular expression pattern for sanitizing search queries
DEFAULT_SANITIZE_PATTERN = (
    "[^\w \d\"#\$%&'\(\)\*\+,-\.\/:;?@\^_`{\|}~]+|\%\w+|;|/|\(|\)"
)

# Default number of search results to skip in Azure search
DEFAULT_AZURE_SEARCH_SKIP = 0

# Default number of search results to return from Azure search
DEFAULT_AZURE_SEARCH_TOP = 10

# Mapping of Azure search result fields to desired output structure.
# Knowledge of the index search result structure is required.
DEFAULT_AZURE_SEARCH_TRANSFORM_MAP_JSON = {
    "id": "/id",
    "title": "/title",
    "score": "/@search.score",
    "url": "/url",
    "content": "/content",
    "last_updated": "/last_updated",
}

# Default Azure search parameters
# Consult https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.searchclient?view=azure-python#azure-search-documents-searchclient-search
DEFAULT_AZURE_SEARCH_PARAMS = {}

# Default number of search results to return from Ailab Llama Search
DEFAULT_AILAB_LLAMA_SEARCH_TOP = 10

# Mapping of Ailab Llama search result fields to desired output structure.
# Knowledge of the index search result structure is required.
DEFAULT_AILAB_LLAMA_SEARCH_TRANS_PATHS = {
    "id": "node/metadata/id",
    "chunk_id": "node/metadata/chunk_id",
    "url": "node/metadata/url",
    "title": "node/metadata/title",
    "subtitle": "node/metadata/subtitle",
    "tokens_count": "node/metadata/tokens_count",
    "last_updated": "node/metadata/last_updated",
    "score": "node/metadata/score",
    "llama_id": "node/id_",
    "llama_score": "score",
    "content": "node/text",
}

# Default Ailab Llama parameters
DEFAULT_AZURE_SEARCH_PARAMS = {}
