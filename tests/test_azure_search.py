import unittest
from unittest.mock import patch

from app.app_creator import create_app
from tests.common import TestConfig


class TestAzureSearch(unittest.TestCase):
    def setUp(self):
        self.config = TestConfig()
        self.app = create_app(self.config)
        self.client = self.app.test_client()

    def test_search_azure_success(self):
        with patch("app.blueprints.search.search") as mock_search:
            mock_search.return_value = {"some": "azure data"}
            response = self.client.post("/search/azure", json={"query": "azure query"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"some": "azure data"})

    def test_search_azure_no_query(self):
        response = self.client.post("/search/azure", json={})
        self.assertEqual(response.status_code, 400)

    def test_search_azure_error(self):
        with patch("app.blueprints.search.search") as mock_search:
            mock_search.side_effect = Exception("Azure search failed")
            response = self.client.post("/search/azure", json={"query": "azure query"})
            self.assertEqual(response.status_code, 500)
