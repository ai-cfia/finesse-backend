import unittest
from accuracy_functions import calculate_accuracy, save_to_markdown, save_to_csv

class TestFunctions(unittest.TestCase):

    def test_calculate_accuracy(self):
        responses_url = ["http://example.com/page1", "http://example.com/page2", "http://example.com/page3", "http://example.com/page4"]
        expected_url = "http://example.com/page2"
        result = calculate_accuracy(responses_url, expected_url)
        self.assertEqual(result.position, 1)
        self.assertEqual(result.total_pages, 4)
        self.assertEqual(result.score, 0.75)
    
if __name__ == "__main__":
    unittest.main()
