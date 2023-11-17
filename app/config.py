import os
from dataclasses import dataclass

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from dotenv import load_dotenv

load_dotenv()


@dataclass
class AzureSearchConfig:
    endpoint = os.getenv("FINESSE_BACKEND_AZURE_SEARCH_ENDPOINT")
    api_key = os.getenv("FINESSE_BACKEND_AZURE_SEARCH_API_KEY")
    index_name = os.getenv("FINESSE_BACKEND_AZURE_SEARCH_INDEX_NAME")
    client = SearchClient(
        os.getenv("FINESSE_BACKEND_AZURE_SEARCH_ENDPOINT"),
        os.getenv("FINESSE_BACKEND_AZURE_SEARCH_INDEX_NAME"),
        AzureKeyCredential(os.getenv("FINESSE_BACKEND_AZURE_SEARCH_API_KEY")),
    )


@dataclass
class Config:
    AZURE_CONFIG = AzureSearchConfig()
