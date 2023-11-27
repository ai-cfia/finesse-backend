import unittest
from unittest.mock import Mock, patch

import requests

from app.finesse_data import (
    EmptyQueryError,
    FinesseDataFetchException,
    fetch_data,
    find_best_match,
)


class TestFetchData(unittest.TestCase):
    def setUp(self):
        self.finesse_data_url = "https://example.com/data"
        self.match_threshold = 90
        self.files = [
            {"name": "file1.json", "download_url": "https://example.com/file1.json"},
            {"name": "file2.json", "download_url": "https://example.com/file2.json"},
        ]
        self.candidates = [
            "Annual Financial Report",
            "Project Proposal March",
            "Client Contact Information",
            "Product Catalog",
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

    def test_exact_match(self):
        result = find_best_match(
            "Annual Financial Report", self.candidates, self.match_threshold
        )
        self.assertEqual(result, "Annual Financial Report")

    def test_misspelled_match(self):
        result = find_best_match(
            "Project Propsal March", self.candidates, self.match_threshold
        )
        self.assertEqual(result, "Project Proposal March")

    def test_transposed_letters_match(self):
        result = find_best_match(
            "Cleint Contact Information", self.candidates, self.match_threshold
        )
        self.assertEqual(result, "Client Contact Information")

    def test_extra_letter_match(self):
        result = find_best_match(
            "Product Catatalog", self.candidates, self.match_threshold
        )
        self.assertEqual(result, "Product Catalog")

    def test_no_match_found(self):
        result = find_best_match(
            "Completely Unrelated String", self.candidates, self.match_threshold
        )
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
