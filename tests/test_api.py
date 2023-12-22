import unittest
from unittest.mock import patch

from app.api.common.ailab_db import DBError
from app.app_creator import create_app
from tests.common import TestConfig


class TestApiV1(unittest.TestCase):
    def setUp(self):
        self.config = TestConfig()
        self.app = create_app(self.config)
        self.client = self.app.test_client()
        self.static_search_url = "/api/v1/search/static"
        self.azure_search_url = "/api/v1/search/azure"
        self.ailab_search_url = "/api/v1/search/ailab"
        self.health_check_url = "/api/v1/health"

    ### Static ###
    def test_search_static_success(self):
        with patch("app.api.v1.blueprints.search.fetch_data") as mock_fetch:
            mock_fetch.return_value = {"some": "data"}
            json = {"query": "test query"}
            response = self.client.post(self.static_search_url, json=json)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"some": "data"})

    def test_search_static_no_query(self):
        response = self.client.post(self.static_search_url, json={})
        self.assertEqual(response.status_code, 400)

    def test_search_static_no_match(self):
        with patch("app.api.v1.blueprints.search.fetch_data") as mock_fetch:
            mock_fetch.return_value = None
            json = {"query": "test query"}
            response = self.client.post(self.static_search_url, json=json)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, None)

    def test_search_static_error(self):
        with patch("app.api.v1.blueprints.search.fetch_data") as mock_fetch:
            mock_fetch.side_effect = Exception("API request failed")
            json = {"query": "test query"}
            response = self.client.post(self.static_search_url, json=json)
            self.assertEqual(response.status_code, 500)

    ### Azure ###
    def test_search_azure_success(self):
        with patch("app.api.v1.blueprints.search.search") as mock_search:
            mock_search.return_value = {"some": "azure data"}
            json = {"query": "azure query"}
            response = self.client.post(self.azure_search_url, json=json)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"some": "azure data"})

    def test_search_azure_no_query(self):
        response = self.client.post(self.azure_search_url, json={})
        self.assertEqual(response.status_code, 400)

    def test_search_azure_error(self):
        with patch("app.api.v1.blueprints.search.search") as mock_search:
            mock_search.side_effect = Exception("Azure search failed")
            json = {"query": "azure query"}
            response = self.client.post(self.azure_search_url, json=json)
            self.assertEqual(response.status_code, 500)

    ### Ailab ###
    def test_search_ailab_success(self):
        with patch("app.api.v1.blueprints.search.ailab_db_search") as mock_search:
            mock_search.return_value = {"some": "ailab data"}
            json = {"query": "ailab query"}
            response = self.client.post(self.ailab_search_url, json=json)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"some": "ailab data"})

    def test_search_ailab_no_query(self):
        response = self.client.post(self.ailab_search_url, json={})
        self.assertEqual(response.status_code, 400)

    def test_search_ailab_db_error(self):
        with patch("app.api.v1.blueprints.search.ailab_db_search") as mock_search:
            mock_search.side_effect = DBError("Ailab DB failed")
            json = {"query": "ailab query"}
            response = self.client.post(self.ailab_search_url, json=json)
            self.assertEqual(response.status_code, 500)

    def test_search_ailab_unexpected_error(self):
        with patch("app.api.v1.blueprints.search.ailab_db_search") as mock_search:
            mock_search.side_effect = Exception("Unexpected error")
            json = {"query": "ailab query"}
            response = self.client.post(self.ailab_search_url, json=json)
            self.assertEqual(response.status_code, 500)

    ### Health ###
    def test_health_route(self):
        response = self.client.get(self.health_check_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "ok")
