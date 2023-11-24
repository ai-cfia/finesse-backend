import os
from dataclasses import dataclass

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv
from index_search import AzureIndexSearchConfig

load_dotenv()

DEFAULT_DEBUG_MODE = "False"


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
