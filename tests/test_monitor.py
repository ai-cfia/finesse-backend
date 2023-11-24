import unittest

from app.app_creator import create_app
from tests.common import TestConfig


class TestMonitor(unittest.TestCase):
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
