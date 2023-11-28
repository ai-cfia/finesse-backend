from dataclasses import dataclass
from unittest.mock import Mock

from app.config import Config


@dataclass
class TestAzureSearchConfig:
    endpoint = "endpoint"
    api_key = "api_key"
    index_name = "index"
    client = Mock()


@dataclass
class TestConfig(Config):
    AZURE_CONFIG = TestAzureSearchConfig()
    FINESSE_DATA_URL = ""
    DEBUG = True
    TESTING = True
