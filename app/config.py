import json
import os
from typing import TypedDict

from ailab_llamaindex_search import create_index_object
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex

import app.constants as constants

load_dotenv()


class Config(TypedDict):
    AZURE_SEARCH_CLIENT: SearchClient
    DEFAULT_AZURE_SEARCH_SKIP: int
    DEFAULT_AZURE_SEARCH_TOP: int
    AZURE_SEARCH_PARAMS: dict
    AZURE_SEARCH_TRANSFORM_MAP: dict
    AILAB_LLAMAINDEX_SEARCH_INDEX: VectorStoreIndex
    AILAB_LLAMAINDEX_SEARCH_PARAMS: dict
    AILAB_LLAMAINDEX_SEARCH_TRANS_PATHS: dict
    DEFAULT_AILAB_LLAMAINDEX_SEARCH_TOP: int
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
        or constants.DEFAULT_AZURE_SEARCH_TRANSFORM_MAP
    )
    azure_search_params = (
        json.loads(os.getenv("FINESSE_BACKEND_AZURE_SEARCH_PARAMS", "{}"))
        or constants.DEFAULT_AZURE_SEARCH_PARAMS
    )
    embed_model_params = json.loads(
        os.getenv("FINESSE_BACKEND_LLAMAINDEX_EMBED_MODEL_PARAMS", "{}")
    )
    vector_store_params = json.loads(
        os.getenv("FINESSE_BACKEND_LLAMAINDEX_VECTOR_STORE_PARAMS", "{}")
    )
    ailab_llamaindex_index = create_index_object(embed_model_params, vector_store_params)
    ailab_llamaindex_search_params = (
        json.loads(os.getenv("FINESSE_BACKEND_AZURE_SEARCH_PARAMS", "{}"))
        or constants.DEFAULT_AILAB_LLAMAINDEX_SEARCH_PARAMS
    )
    ailab_llamaindex_trans_paths = (
        json.loads(os.getenv("FINESSE_BACKEND_LLAMAINDEX_TRANS_PATHS", "{}"))
        or constants.DEFAULT_AILAB_LLAMAINDEX_SEARCH_TRANS_PATHS
    )

    return {
        "DEFAULT_AZURE_SEARCH_SKIP": constants.DEFAULT_AZURE_SEARCH_SKIP,
        "DEFAULT_AZURE_SEARCH_TOP": constants.DEFAULT_AZURE_SEARCH_TOP,
        "AZURE_SEARCH_CLIENT": azure_search_client,
        "AZURE_SEARCH_PARAMS": azure_search_params,
        "AZURE_SEARCH_TRANSFORM_MAP": azure_search_transform_map,
        "AILAB_LLAMAINDEX_SEARCH_INDEX": ailab_llamaindex_index,
        "AILAB_LLAMAINDEX_SEARCH_PARAMS": ailab_llamaindex_search_params,
        "AILAB_LLAMAINDEX_SEARCH_TRANS_PATHS": ailab_llamaindex_trans_paths,
        "DEFAULT_AILAB_LLAMAINDEX_SEARCH_TOP": constants.DEFAULT_AILAB_LLAMAINDEX_SEARCH_TOP,
        "FINESSE_DATA_URL": os.getenv("FINESSE_BACKEND_STATIC_FILE_URL"),
        "DEBUG": os.getenv(
            "FINESSE_BACKEND_DEBUG_MODE", constants.DEFAULT_DEBUG_MODE
        ).lower()
        == "true",
        "ERROR_EMPTY_QUERY": os.getenv(
            "FINESSE_BACKEND_ERROR_EMPTY_QUERY", constants.DEFAULT_ERROR_EMPTY_QUERY
        ),
        "ERROR_AZURE_FAILED": os.getenv(
            "FINESSE_BACKEND_ERROR_AZURE_FAILED", constants.DEFAULT_ERROR_AZURE_FAILED
        ),
        "ERROR_FINESSE_DATA_FAILED": os.getenv(
            "FINESSE_BACKEND_ERROR_FINESSE_DATA_FAILED",
            constants.DEFAULT_ERROR_FINESSE_DATA_FAILED,
        ),
        "ERROR_AILAB_FAILED": os.getenv(
            "FINESSE_BACKEND_ERROR_AILAB_FAILED", constants.DEFAULT_ERROR_AILAB_FAILED
        ),
        "ERROR_UNEXPECTED": os.getenv(
            "FINESSE_BACKEND_ERROR_UNEXPECTED", constants.DEFAULT_ERROR_UNEXPECTED
        ),
        "FUZZY_MATCH_THRESHOLD": int(
            os.getenv(
                "FINESSE_BACKEND_FUZZY_MATCH_THRESHOLD",
                str(constants.DEFAULT_FUZZY_MATCH_THRESHOLD),
            )
        ),
        "SANITIZE_PATTERN": os.getenv(
            "FINESSE_BACKEND_SANITIZE_PATTERN", constants.DEFAULT_SANITIZE_PATTERN
        ),
    }
