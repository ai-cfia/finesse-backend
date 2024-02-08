import unittest
from unittest.mock import patch

from app.ailab_db import DBError
from app.app_creator import create_app
from app.config import (
    DEFAULT_ERROR_AILAB_FAILED,
    DEFAULT_ERROR_EMPTY_QUERY,
    DEFAULT_ERROR_UNEXPECTED,
    DEFAULT_SANITIZE_PATTERN,
    Config,
)


class TestAilabSearch(unittest.TestCase):
    def setUp(self):
        self.config: Config = {
            "DEBUG": True,
            "TESTING": True,
            "SANITIZE_PATTERN": DEFAULT_SANITIZE_PATTERN,
            "ERROR_AILAB_FAILED": DEFAULT_ERROR_AILAB_FAILED,
            "ERROR_UNEXPECTED": DEFAULT_ERROR_UNEXPECTED,
            "ERROR_EMPTY_QUERY": DEFAULT_ERROR_EMPTY_QUERY,
        }
        self.app = create_app(self.config)
        self.client = self.app.test_client()

    def test_search_ailab_success(self):
        with patch("app.blueprints.search.ailab_db_search") as mock_search:
            mock_search.return_value = {"some": "ailab data"}
            response = self.client.post("/search/ailab", json={"query": "ailab query"})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"some": "ailab data"})

    def test_search_ailab_no_query(self):
        response = self.client.post("/search/ailab", json={})
        self.assertEqual(response.status_code, 400)

    def test_search_ailab_db_error(self):
        with patch("app.blueprints.search.ailab_db_search") as mock_search:
            mock_search.side_effect = DBError("Ailab DB failed")
            response = self.client.post("/search/ailab", json={"query": "ailab query"})
            self.assertEqual(response.status_code, 500)

    def test_search_ailab_unexpected_error(self):
        with patch("app.blueprints.search.ailab_db_search") as mock_search:
            mock_search.side_effect = Exception("Unexpected error")
            response = self.client.post("/search/ailab", json={"query": "ailab query"})
            self.assertEqual(response.status_code, 500)
