from dataclasses import dataclass
from unittest.mock import Mock


@dataclass
class TestAzureSearchConfig:
    endpoint = "endpoint"
    api_key = "api_key"
    index_name = "index"
    client = Mock()
