import unittest
from unittest.mock import patch

from app.app_creator import create_app
from tests.common import TestConfig


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.config = TestConfig()
        self.app = create_app(self.config)
        self.client = self.app.test_client()

    def test_search_static_success(self):
        with patch("app.blueprints.search.fetch_data") as mock_fetch:
            mock_fetch.return_value = {"some": "data"}
            response = self.client.post("/search/static", json={"query": "test query"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"some": "data"})

    def test_search_static_no_query(self):
        response = self.client.post("/search/static", json={})
        self.assertEqual(response.status_code, 400)

    def test_search_static_no_match(self):
        with patch("app.blueprints.search.fetch_data") as mock_fetch:
            mock_fetch.return_value = None
            response = self.client.post("/search/static", json={"query": "test query"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, None)

    def test_search_static_error(self):
        with patch("app.blueprints.search.fetch_data") as mock_fetch:
            mock_fetch.side_effect = Exception("API request failed")
            response = self.client.post("/search/static", json={"query": "test query"})
            self.assertEqual(response.status_code, 500)

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
