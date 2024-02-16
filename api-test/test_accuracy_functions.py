import unittest
from accuracy_functions import calculate_accuracy, save_to_markdown, save_to_csv

class TestFunctions(unittest.TestCase):

    def test_calculate_accuracy(self):
        responses_url = ["http://example.com/page1", "http://example.com/page2", "http://example.com/page3"]
        expected_url = "http://example.com/page2"
        result = calculate_accuracy(responses_url, expected_url)
        self.assertEqual(result.position, 1)
        self.assertEqual(result.total_pages, 3)
        self.assertAlmostEqual(result.score, 0.6666666666666667)

    def test_save_to_markdown(self):
        test_data = {
            "file1": {
                "question": "What is Python?",
                "expected_page": {"url": "http://example.com/page1"},
                "accuracy": 0.8,
                "time": 100
            }
        }
        engine = "test_engine"
        save_to_markdown(test_data, engine)

    def test_save_to_csv(self):
        test_data = {
            "file1": {
                "question": "What is Python?",
                "expected_page": {"url": "http://example.com/page1"},
                "accuracy": 0.8,
                "time": 100
            }
        }
        engine = "test_engine"
        save_to_csv(test_data, engine)

if __name__ == "__main__":
    unittest.main()
