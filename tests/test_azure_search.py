import unittest
from unittest.mock import patch

from app.azure_search import AzureSearchQueryError, search_documents
from tests.common import TestAzureSearchConfig


class TestAzureSearch(unittest.TestCase):
    def setUp(self):
        self.config = TestAzureSearchConfig()

    def test_search_documents_empty_query(self):
        results = search_documents("", self.config)
        self.assertEqual(results, [])

    @patch("app.azure_search.logging")
    def test_search_documents_query_error(self, mock_logging):
        self.config.client.search.side_effect = Exception("Search failed")
        with self.assertRaises(AzureSearchQueryError):
            search_documents("test_query", self.config)
        mock_logging.error.assert_called()


if __name__ == "__main__":
    unittest.main()
