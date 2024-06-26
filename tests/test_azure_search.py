import unittest
from unittest.mock import Mock, patch

from app.app_creator import create_app
from app.blueprints.search import AzureIndexSearchError
from app.config import Config
from app.constants import (
    DEFAULT_AZURE_SEARCH_PARAMS,
    DEFAULT_AZURE_SEARCH_SKIP,
    DEFAULT_AZURE_SEARCH_TOP,
    DEFAULT_AZURE_SEARCH_TRANSFORM_MAP,
    DEFAULT_ERROR_AZURE_FAILED,
    DEFAULT_ERROR_EMPTY_QUERY,
    DEFAULT_ERROR_UNEXPECTED,
    DEFAULT_SANITIZE_PATTERN,
)


class TestAzureSearch(unittest.TestCase):
    def setUp(self):
        self.config: Config = {
            "DEBUG": True,
            "TESTING": True,
            "DEFAULT_AZURE_SEARCH_SKIP": DEFAULT_AZURE_SEARCH_SKIP,
            "DEFAULT_AZURE_SEARCH_TOP": DEFAULT_AZURE_SEARCH_TOP,
            "AZURE_SEARCH_PARAMS": DEFAULT_AZURE_SEARCH_PARAMS,
            "AZURE_SEARCH_CLIENT": Mock(),
            "SANITIZE_PATTERN": DEFAULT_SANITIZE_PATTERN,
            "ERROR_UNEXPECTED": DEFAULT_ERROR_UNEXPECTED,
            "ERROR_EMPTY_QUERY": DEFAULT_ERROR_EMPTY_QUERY,
            "ERROR_AZURE_FAILED": DEFAULT_ERROR_AZURE_FAILED,
            "AZURE_SEARCH_TRANSFORM_MAP": DEFAULT_AZURE_SEARCH_TRANSFORM_MAP,
        }
        self.app = create_app(self.config)
        self.client = self.app.test_client()

    def test_search_azure_success(self):
        with patch("app.blueprints.search.search") as mock_search:
            mock_search.return_value = {"some": "azure data"}
            response = self.client.post(
                "/search/azure",
                json={"query": "azure query"},
                query_string={"skip": 1, "top": 5},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"some": "azure data"})
            mock_search.assert_called_with(
                "azure query",
                self.config["AZURE_SEARCH_CLIENT"],
                {"skip": 1, "top": 5, **self.config["AZURE_SEARCH_PARAMS"]},
                self.config["AZURE_SEARCH_TRANSFORM_MAP"],
            )

    def test_search_azure_success_with_defaults(self):
        """should use default skip and top when not provided"""
        with patch("app.blueprints.search.search") as mock_search:
            mock_search.return_value = {"some": "default azure data"}
            response = self.client.post(
                "/search/azure", json={"query": "default azure query"}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"some": "default azure data"})
            mock_search.assert_called_with(
                "default azure query",
                self.config["AZURE_SEARCH_CLIENT"],
                {
                    "skip": self.config["DEFAULT_AZURE_SEARCH_SKIP"],
                    "top": self.config["DEFAULT_AZURE_SEARCH_TOP"],
                    **self.config["AZURE_SEARCH_PARAMS"],
                },
                self.config["AZURE_SEARCH_TRANSFORM_MAP"],
            )

    def test_search_azure_no_query(self):
        response = self.client.post("/search/azure", json={})
        self.assertEqual(response.status_code, 400)

    def test_search_azure_error(self):
        with patch("app.blueprints.search.search") as mock_search:
            mock_search.side_effect = AzureIndexSearchError("Azure search failed")
            response = self.client.post("/search/azure", json={"query": "azure query"})
            self.assertEqual(response.status_code, 500)

    def test_search_azure_with_semantic_params(self):
        """Test search with semantic search parameters."""
        finesse_backend_azure_search_params = {
            "highlight_fields": "content",
            "highlight_pre_tag": "<strong>",
            "highlight_post_tag": "</strong>",
            "query_type": "semantic",
            "semantic_configuration_name": "Semantic-config-public-guidance-docs",
        }

        # Temporarily update AZURE_SEARCH_PARAMS for this test
        original_azure_search_params = self.config["AZURE_SEARCH_PARAMS"]
        self.config["AZURE_SEARCH_PARAMS"].update(finesse_backend_azure_search_params)

        with patch("app.blueprints.search.search") as mock_search:
            mock_search.return_value = {"some": "semantic azure data"}
            response = self.client.post(
                "/search/azure", json={"query": "semantic azure query"}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"some": "semantic azure data"})
            mock_search.assert_called_with(
                "semantic azure query",
                self.config["AZURE_SEARCH_CLIENT"],
                {
                    "skip": self.config["DEFAULT_AZURE_SEARCH_SKIP"],
                    "top": self.config["DEFAULT_AZURE_SEARCH_TOP"],
                    **self.config["AZURE_SEARCH_PARAMS"],
                },
                self.config["AZURE_SEARCH_TRANSFORM_MAP"],
            )

        expected_params = finesse_backend_azure_search_params
        actual_params = mock_search.call_args[0][2]
        for key in expected_params.keys():
            self.assertIn(key, actual_params)
            self.assertEqual(actual_params[key], expected_params[key])

        # Reset AZURE_SEARCH_PARAMS to original after test to avoid side effects
        self.config["AZURE_SEARCH_PARAMS"] = original_azure_search_params
