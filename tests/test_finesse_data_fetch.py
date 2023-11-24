import unittest
from unittest.mock import Mock, patch

import requests

from app.finesse_data import EmptyQueryError, FinesseDataFetchException, fetch_data


class TestFetchData(unittest.TestCase):
    def setUp(self):
        self.finesse_data_url = "https://example.com/data"
        self.match_threshold = 90
        self.files = [
            {"name": "file1.json", "download_url": "https://example.com/file1.json"},
            {"name": "file2.json", "download_url": "https://example.com/file2.json"},
        ]

    @patch("app.finesse_data.requests.get")
    def test_fetch_data_empty_query(self, mock_get):
        with self.assertRaises(EmptyQueryError):
            fetch_data(self.finesse_data_url, "", self.match_threshold)

    @patch("app.finesse_data.requests.get")
    def test_fetch_data_no_match_found(self, mock_get):
        mock_get.return_value = Mock(status_code=200, json=lambda: self.files)
        result = fetch_data(self.finesse_data_url, "bad query", self.match_threshold)
        self.assertIsNone(result)

    @patch("app.finesse_data.requests.get")
    def test_fetch_data_success(self, mock_get):
        mock_get.side_effect = [
            Mock(status_code=200, json=lambda: self.files),
            Mock(status_code=200, json=lambda: {"data": "content"}),
        ]
        result = fetch_data(self.finesse_data_url, "file1", self.match_threshold)
        self.assertEqual(result, {"data": "content"})

    @patch("app.finesse_data.requests.get")
    def test_fetch_data_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException()
        with self.assertRaises(FinesseDataFetchException):
            fetch_data(self.finesse_data_url, "a query", self.match_threshold)


if __name__ == "__main__":
    unittest.main()
