# tests/test_main.py
import unittest
from src.app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_read_root(self):
        response = self.app.get('/')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('current_time' in data)
        self.assertIsInstance(data['current_time'], int)
