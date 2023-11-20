import unittest
from unittest.mock import patch

from app.azure_search import (
    AzureSearchQueryError,
    EmptyQueryError,
    azure_search_documents,
)
from tests.common import TestAzureSearchConfig


class TestAzureSearch(unittest.TestCase):
    def setUp(self):
        self.config = TestAzureSearchConfig()

    def test_search_documents_empty_query(self):
        with self.assertRaises(EmptyQueryError):
            azure_search_documents("", self.config)

    @patch("app.azure_search.logging")
    def test_search_documents_query_error(self, mock_logging):
        self.config.client.search.side_effect = Exception("Search failed")
        with self.assertRaises(AzureSearchQueryError):
            azure_search_documents("test_query", self.config)
        mock_logging.error.assert_called()


if __name__ == "__main__":
    unittest.main()
