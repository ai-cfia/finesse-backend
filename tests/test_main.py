import unittest
from dataclasses import dataclass

from app.app_creator import create_app
from app.azure_search import AzureSearchConfig
from app.config import Config


@dataclass
class TestAzureConfig(AzureSearchConfig):
    endpoint = ""
    api_key = ""
    index_name = ""
    client = None


@dataclass
class TestConfig(Config):
    app_config = TestAzureConfig()


class TestApp(unittest.TestCase):
    def setUp(self):
        self.config = TestConfig()
        self.app = create_app(self.config)
        self.client = self.app.test_client()

    def test_read_root(self):
        response = self.client.get("/")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue("current_time" in data)
        self.assertIsInstance(data["current_time"], int)
        self.assertTrue("current_time" in data)
        self.assertIsInstance(data["current_time"], int)
        self.assertIsInstance(data["current_time"], int)
        self.assertIsInstance(data["current_time"], int)
