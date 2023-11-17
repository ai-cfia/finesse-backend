from dataclasses import dataclass
from unittest.mock import Mock

from app.config import AzureSearchConfig


@dataclass
class TestAzureSearchConfig(AzureSearchConfig):
    endpoint = "endpoint"
    api_key = "api_key"
    index_name = "index"
    client = Mock()
