import unittest
from unittest.mock import Mock, patch

from ailab_llamaindex_search import AilabLlamaIndexSearchError

from app import constants
from app.app_creator import create_app
from app.config import Config


class TestAilabLLamaIndexSearch(unittest.TestCase):
    def setUp(self):
        self.config: Config = {
            "DEBUG": True,
            "TESTING": True,
            "SANITIZE_PATTERN": constants.DEFAULT_SANITIZE_PATTERN,
            "ERROR_UNEXPECTED": constants.DEFAULT_ERROR_UNEXPECTED,
            "ERROR_EMPTY_QUERY": constants.DEFAULT_ERROR_EMPTY_QUERY,
            "AILAB_LLAMAINDEX_SEARCH_INDEX": Mock(),
            "AILAB_LLAMAINDEX_SEARCH_TRANS_PATHS": constants.DEFAULT_AILAB_LLAMAINDEX_SEARCH_TRANS_PATHS,
            "DEFAULT_AILAB_LLAMAINDEX_SEARCH_TOP": constants.DEFAULT_AILAB_LLAMAINDEX_SEARCH_TOP,
        }
        self.app = create_app(self.config)
        self.client = self.app.test_client()

    def test_search_llamaindex_success(self):
        with patch("app.blueprints.search.llamaindex_search") as mock_search:
            mock_search.return_value = {"some": "data"}
            response = self.client.post(
                "/search/llamaindex",
                json={"query": "some query"},
                query_string={"top": 5},
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"some": "data"})
            mock_search.assert_called_with(
                "some query",
                self.config["AILAB_LLAMAINDEX_SEARCH_INDEX"],
                5,
                self.config["AILAB_LLAMAINDEX_SEARCH_TRANS_PATHS"],
            )

    def test_search_llamaindex_success_with_defaults(self):
        """should use default top when not provided"""
        with patch("app.blueprints.search.llamaindex_search") as mock_search:
            mock_search.return_value = {"some": "data"}
            response = self.client.post(
                "/search/llamaindex", json={"query": "some query"}
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"some": "data"})
            mock_search.assert_called_with(
                "some query",
                self.config["AILAB_LLAMAINDEX_SEARCH_INDEX"],
                self.config["DEFAULT_AILAB_LLAMAINDEX_SEARCH_TOP"],
                self.config["AILAB_LLAMAINDEX_SEARCH_TRANS_PATHS"],
            )

    def test_search_llamaindex_no_query(self):
        response = self.client.post("/search/llamaindex", json={})
        self.assertEqual(response.status_code, 400)

    def test_search_llamaindex_error(self):
        with patch("app.blueprints.search.search") as mock_search:
            mock_search.side_effect = AilabLlamaIndexSearchError("search failed.")
            response = self.client.post(
                "/search/llamaindex", json={"query": "some query"}
            )
            self.assertEqual(response.status_code, 500)
