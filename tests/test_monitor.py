import unittest
from dataclasses import dataclass

from app.app_creator import create_app
from app.config import Config
from tests.common import TestAzureSearchConfig


@dataclass
class TestConfig(Config):
    app_config = TestAzureSearchConfig()


class TestMonitorBlueprint(unittest.TestCase):
    def setUp(self):
        self.config = TestConfig()
        self.app = create_app(self.config)
        self.client = self.app.test_client()

    def test_health_route(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "ok")


if __name__ == "__main__":
    unittest.main()
